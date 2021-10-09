import os

import ramda as R
from moonleap.utils.case import u0
from titan.react_pkg.pkg.ml_get import ml_react_app
from titan.react_view_pkg.router.resources import concat_router_configs


def _group_by(get_key, xs):
    acc = []
    for x in xs:
        key = get_key(x)
        group = R.find(lambda x: x[0] == key, acc)
        if not group:
            group = [key, []]
            acc.append(group)
        group[1].append(x)
    return acc


def _move_url_values_up(route_configs):
    urls = [x.url for x in route_configs if x.url]
    for x in route_configs:
        x.url = urls.pop(0) if urls else None
    return route_configs


def _append(x, indent, result):
    result.append(" " * (indent) + x)


def _needs_switch(routes_by_first_component_and_url, level):
    count_routes = 0
    for _, group in routes_by_first_component_and_url:
        router_config = group[0][level]
        count_routes += 1 if router_config.url else 0
    return count_routes > 1


def _group_routes(level, routes):
    # all the routes that share their first component should be grouped inside a
    # route for that first component
    def get_component_and_url(route):
        router_config = route[level]
        return (router_config.component, router_config.url)

    return _group_by(get_component_and_url, routes)


def render_routes(routes, url, level, indent, result):
    routes_by_first_component_and_url = _group_routes(level, routes)
    needs_switch = _needs_switch(routes_by_first_component_and_url, level)

    if needs_switch:
        _append("<Switch>", indent, result)
        indent += 2

    for _, group in routes_by_first_component_and_url:
        router_config = group[0][level]
        next_routes = [x for x in group if len(x) > level + 1]
        url_memo = url
        if router_config.url:
            url += "/" + router_config.url
            postfix = (
                "/" if [route for route in next_routes if route[level + 1].url] else ""
            )
            _append(f'<Route path="{url}{postfix}">', indent, result)
            indent += 2

        if router_config.wraps:
            _append(f"<{u0(router_config.component.name)}>", indent, result)
            indent += 2
        else:
            _append(f"<{u0(router_config.component.name)}/>", indent, result)

        render_routes(
            next_routes,
            url,
            level + 1,
            indent,
            result,
        )

        if router_config.wraps:
            indent -= 2
            _append(f"</{u0(router_config.component.name)}>", indent, result)

        if router_config.url:
            url = url_memo
            indent -= 2
            _append("</Route>", indent, result)

    if needs_switch:
        indent -= 2
        _append("</Switch>", indent, result)


def _routed_components(modules):
    result = []
    for module in modules:
        for component in module.routed_components:
            if component not in result:
                result.append(component)

    return result


def _routes(routed_components):
    routes = []

    def add(route):
        tail_component = route[-1].component

        wrapped_components = tail_component.wrapped_components
        if not wrapped_components:
            routes.append(route)  # _move_url_values_up(route)
            return

        for wrapped_child in wrapped_components:
            more_router_configs = wrapped_child.create_router_configs()
            if more_router_configs:
                add(concat_router_configs(route, more_router_configs))

    for routed_component in routed_components:
        route = routed_component.create_router_configs()
        if route:
            add(route)

    return routes


def _components_used_in_router(routes):
    result = []

    def add(component):
        queue = [component]
        while queue:
            component = queue.pop()
            if component not in result:
                result.append(component)
            queue.extend(component.wrapped_components)

    for route in routes:
        for router_config in route:
            add(router_config.component)

    return result


def get_context(router):
    _ = lambda: None
    _.react_app = ml_react_app(router)
    _.routed_components = _routed_components(_.react_app.modules)
    _.routes = _routes(_.routed_components)

    class Sections:
        def route_imports(self):
            used_components = _components_used_in_router(_.routes)

            result = []
            imports_by_module_name = R.group_by(
                lambda x: x.module.name, used_components
            )
            for module_name, components in imports_by_module_name.items():
                component_names = ", ".join(R.map(lambda x: x.name)(components))
                result.append(
                    f"import {{ {component_names} }} from 'src/{module_name}/components';"
                )
            return os.linesep.join(result)

        def routes(self):
            result = []
            render_routes(_.routes, "", 0, 6, result)
            return os.linesep.join(result)

    return dict(sections=Sections())
