import os
import typing as T
from dataclasses import dataclass

import ramda as R
from moonleap.utils.case import u0
from titan.react_pkg.router.resources import RouterConfig, prepend_router_configs


@dataclass
class Route:
    configs: T.List[RouterConfig]


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


class Sections:
    def __init__(self, res):
        self.res = res

    def route_imports(self):
        components = []

        def add(component):
            queue = [component]
            while queue:
                component = queue.pop()
                if component not in components:
                    components.append(component)
                queue.extend(component.wrapped_child_components)

        for module in self.res.module.react_app.modules:
            for component in module.routed_components:
                for router_config in component.create_router_configs():
                    add(router_config.component)

        result = []
        imports_by_module_name = R.group_by(lambda x: x.module.name, components)
        for module_name, components in imports_by_module_name.items():
            component_names = ", ".join(R.map(lambda x: x.name)(components))
            result.append(
                f"import {{ {component_names} }} from 'src/{module_name}/components';"
            )

        return os.linesep.join(result)

    def routes(self):
        routes = []

        for module in self.res.module.react_app.modules:
            for component in module.routed_components:
                router_configs = component.create_router_configs()
                if router_configs:
                    add_route(router_configs, routes)

        result = []
        add_result(routes, "", 0, 6, result)

        result_str = os.linesep.join(result)
        return result_str


def add_route(router_configs, routes):
    wrapped_child_components = router_configs[-1].component.wrapped_child_components
    if not wrapped_child_components:
        routes.append(Route(configs=_move_url_values_up(router_configs)))
        return

    for wrapped_child in wrapped_child_components:
        more_router_configs = wrapped_child.create_router_configs()
        if more_router_configs:
            add_route(
                prepend_router_configs(router_configs, more_router_configs), routes
            )


def _needs_switch(routes_by_first_component_and_url, level):
    count_routes = 0
    for _, group in routes_by_first_component_and_url:
        router_config = group[0].configs[level]
        count_routes += 1 if router_config.url else 0
    return count_routes > 1


def add_result(routes, url, level, indent, result):
    # all the routes that share their first component should be grouped inside a
    # route for that first component
    def get_component_and_url(route):
        router_config = route.configs[level]
        return (router_config.component, router_config.url)

    routes_by_first_component_and_url = _group_by(get_component_and_url, routes)
    needs_switch = _needs_switch(routes_by_first_component_and_url, level)

    if needs_switch:
        _append("<Switch>", indent, result)
        indent += 2

    for _, group in routes_by_first_component_and_url:
        router_config = group[0].configs[level]
        next_routes = [x for x in group if len(x.configs) > level + 1]
        url_memo = url
        if router_config.url:
            url += "/" + router_config.url
            postfix = (
                "/"
                if [route for route in next_routes if route.configs[level + 1].url]
                else ""
            )
            _append(f'<Route path="{url}{postfix}">', indent, result)
            indent += 2

        if router_config.wraps:
            _append(f"<{u0(router_config.component.name)}>", indent, result)
            indent += 2
        else:
            _append(f"<{u0(router_config.component.name)}/>", indent, result)

        add_result(
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


def get_context(self):
    return dict(sections=Sections(self))
