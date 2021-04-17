import os

import ramda as R
from moonleap.utils.case import title0


def get_route_imports(self):
    router_configs = self.module.router_configs.merged
    imports_by_module_name = R.pipe(
        R.always(router_configs),
        R.group_by(lambda x: x.module.name),
    )(None)

    result = []
    for module_name, router_configs in imports_by_module_name.items():
        components = ", ".join(R.map(lambda x: x.component.name)(router_configs))
        result.append(f"import {{ {components} }} from 'src/{module_name}/components'")

    return os.linesep.join(result)


def get_parent_url(router_configs, url):
    result = None
    for router_config in router_configs:
        component = router_config.component
        if url.startswith(component.url):
            if result is None or len(result) < len(component.url):
                if url != component.url:
                    result = component.url
    return result


def get_url_to_parent_url(router_configs):
    result = {}
    for router_config in router_configs:
        component = router_config.component
        parent_url = get_parent_url(router_configs, component.url)
        if parent_url:
            result[component.url] = parent_url
    return result


def get_routes(self):
    router_configs = self.module.router_configs.merged
    url_to_parent_url = get_url_to_parent_url(router_configs)
    result = []

    def get_child_router_configs(router_config):
        return [
            x
            for x in router_configs
            if url_to_parent_url.get(x.component.url) == router_config.component.url
        ]

    def add_routes(router_config, indent=0):
        component = router_config.component
        result.append(" " * indent + f'<Route path="{component.url}">')
        result.append(" " * (indent + 2) + f"<{title0(component.name)}/>")
        child_router_configs = get_child_router_configs(router_config)

        if router_config.wraps:
            result.append(" " * (indent + 2) + "<Switch>")
            for child_router_config in child_router_configs:
                add_routes(child_router_config, indent + 4)
            result.append(" " * (indent + 2) + "</Switch>")

        result.append(" " * indent + "</Route>")

        if not router_config.wraps:
            for child_router_config in child_router_configs:
                add_routes(child_router_config, indent)

    for router_config in router_configs:
        if not url_to_parent_url.get(router_config.component.url):
            add_routes(router_config, indent=8)

    return os.linesep.join(result)
