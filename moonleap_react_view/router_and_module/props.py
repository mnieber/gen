from slugify import slugify


def create_component_router_config(component, url=None, wraps=False):
    from moonleap_react_view.router.resources import RouterConfig

    slug = slugify(component.name)
    return RouterConfig(
        component=component, url=f"{slug if url is None else url}", wraps=wraps
    )
