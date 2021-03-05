import os

import ramda as R
from moonleap.utils.case import title0
from moonleap.utils.inflect import plural


def get_route_imports(self):
    router_configs = self.module.service.router_configs.merged
    imports_by_module_name = R.pipe(
        R.always(router_configs),
        R.group_by(R.prop("module_name")),
    )(None)

    result = []
    for module_name, router_configs in imports_by_module_name.items():
        components = ", ".join(R.map(R.prop("component_name"))(router_configs))
        result.append(f"import {{ {components} }} from 'src/{module_name}/components'")

    return os.linesep.join(result)


def get_parent_url(router_configs, url):
    result = None
    for route_config in router_configs:
        if url.startswith(route_config.url):
            if result is None or len(result) < len(route_config.url):
                if url != route_config.url:
                    result = route_config.url
    return result


def get_url_to_parent_url(router_configs):
    result = {}
    for route_config in router_configs:
        parent_url = get_parent_url(router_configs, route_config.url)
        if parent_url:
            result[route_config.url] = parent_url
    return result


def get_routes(self):
    router_configs = self.module.service.router_configs.merged
    url_to_parent_url = get_url_to_parent_url(router_configs)
    result = []

    def get_child_router_configs(route_config):
        return [
            x
            for x in router_configs
            if url_to_parent_url.get(x.url) == route_config.url
        ]

    def add_routes(route_config, indent=0):
        result.append(" " * indent + f'<Route path="{route_config.url}">')
        result.append(" " * (indent + 2) + f"<{title0(route_config.component_name)}/>")
        child_route_configs = get_child_router_configs(route_config)

        if route_config.wraps:
            result.append(" " * (indent + 2) + f"<Switch>")
            for child_route_config in child_route_configs:
                add_routes(child_route_config, indent + 4)
            result.append(" " * (indent + 2) + f"</Switch>")

        result.append(" " * indent + f"</Route>")

        if not route_config.wraps:
            for child_route_config in child_route_configs:
                add_routes(child_route_config, indent)

    for route_config in router_configs:
        if not url_to_parent_url.get(route_config.url):
            add_routes(route_config, indent=8)

    return os.linesep.join(result)
