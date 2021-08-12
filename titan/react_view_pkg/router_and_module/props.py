from slugify import slugify


def create_component_router_config(component, url=None, wraps=False):
    from titan.react_view_pkg.router.resources import RouterConfig

    slug = slugify(component.name)
    return RouterConfig(
        component=component, url=f"{slug if url is None else url}", wraps=wraps
    )
