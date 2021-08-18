import os

from slugify import slugify


def create_component_router_config(component, url=None, wraps=False):
    from titan.react_pkg.router.resources import RouterConfig

    slug = slugify(component.name)
    return RouterConfig(
        component=component, url=f"{slug if url is None else url}", wraps=wraps
    )


def p_section_route_table_imports(self):
    result = []
    for route_table in self.route_tables.merged:
        result.append(
            f"import {{ routeTable as {route_table.name}RouteTable }}"
            + f" from '{route_table.import_path}';"
        )
    return os.linesep.join(result)