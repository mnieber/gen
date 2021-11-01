import os


def get_context(routes_module):
    _ = lambda: None
    _.route_tables = routes_module.react_app.app_module.route_tables.merged

    class Sections:
        def route_table_imports(self):
            result = []
            for route_table in _.route_tables:
                result.append(
                    f"import {{ routeTable as {route_table.name}RouteTable }}"
                    + f" from '{route_table.import_path}';"
                )
            return os.linesep.join(result)

    return dict(sections=Sections(), _=_)
