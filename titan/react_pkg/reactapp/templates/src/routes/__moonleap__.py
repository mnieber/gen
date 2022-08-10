import os


def get_helpers(_):
    class Helpers:
        route_tables = []

        def route_table_imports(self):
            result = []
            for route_table in self.route_tables:
                result.append(
                    f"import {{ routeTable as {route_table.name}RouteTable }}"
                    + f" from '{route_table.import_path}';"
                )
            return os.linesep.join(result)

        def __init__(self):
            for module in _.react_app.modules:
                self.route_tables.extend(module.route_tables)

    return Helpers()
