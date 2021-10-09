from slugify import slugify
from titan.react_view_pkg.router.resources import RouterConfig


def create_component_router_config(component, url=None, wraps=False):

    slug = slugify(component.name)
    return RouterConfig(
        component=component, url=f"{slug if url is None else url}", wraps=wraps
    )
