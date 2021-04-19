import os
import uuid
from dataclasses import dataclass, field

import ramda as R
from moonleap.utils.case import title0
from moonleap_react_view.router.resources import RouterConfig, prepend_router_configs
from slugify import slugify


def group_by(get_key, xs):
    acc = []
    for x in xs:
        key = get_key(x)
        group = R.find(lambda x: x[0] is key, acc)
        if not group:
            group = [key, []]
            acc.append(group)
        group[1].append(x)
    return acc


def get_route_imports(self):
    components = []
    for module in self.module.service.modules:
        for component in module.routed_components:
            for router_config in component.create_router_configs():
                if router_config.component not in components:
                    components.append(router_config.component)

    result = []
    imports_by_module_name = R.group_by(lambda x: x.module.name, components)
    for module_name, components in imports_by_module_name.items():
        component_names = ", ".join(R.map(lambda x: x.name)(components))
        result.append(
            f"import {{ {component_names} }} from 'src/{module_name}/components'"
        )

    return os.linesep.join(result)


def _append(x, indent, result):
    result.append(" " * (indent) + x)


@dataclass
class Route:
    configs: [RouterConfig]

    @property
    def components(self):
        return [x.component for x in self.configs]

    id: str = field(default_factory=lambda: uuid.uuid4().hex, init=False)


def get_routes(self):
    routes = []

    for module in self.module.service.modules:
        for component in module.routed_components:
            router_configs = component.create_router_configs()
            if router_configs:
                add_route(router_configs, routes)

    result = []
    add_result(routes, "", 0, 8, result)

    result_str = os.linesep.join(result)
    return result_str


def add_route(router_configs, routes):
    wrapped_children = router_configs[-1].component.wrapped_children
    if not wrapped_children:
        routes.append(Route(configs=router_configs))
        return

    for wrapped_child in wrapped_children:
        more_router_configs = wrapped_child.create_router_configs()
        if more_router_configs:
            add_route(
                prepend_router_configs(router_configs, more_router_configs), routes
            )


def add_result(routes, url, level, indent, result):
    routes_by_first_component = group_by(lambda x: x.components[level], routes)

    for _, group in routes_by_first_component:
        router_config = group[0].configs[level]
        url_memo = url
        if router_config.url:
            url += "/" + router_config.url
            _append(f'<Route path="{url}/">', indent, result)
            indent += 2

        if not router_config.wraps:
            _append(f"<{title0(router_config.component.name)}/>", indent, result)

        if router_config.wraps:
            _append(f"<{title0(router_config.component.name)}>", indent, result)
            indent += 2

        add_result(
            [x for x in group if len(x.configs) > level + 1],
            url,
            level + 1,
            indent,
            result,
        )

        if router_config.wraps:
            indent -= 2
            _append(f"</{title0(router_config.component.name)}>", indent, result)

        if router_config.url:
            url = url_memo
            indent -= 2
            _append(f"</Route>", indent, result)
