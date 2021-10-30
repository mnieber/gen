def create_router_configs(self, named_component):
    from titan.react_pkg.component.resources import get_component_base_url
    from titan.react_view_pkg.router import RouterConfig

    base_url = get_component_base_url(self, "")
    url = "/".join(([base_url] if base_url else []))
    router_config = RouterConfig(
        component=named_component, url=url, wraps=bool(self.wrapped_components)
    )
    return [router_config]
