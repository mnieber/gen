import os


class Sections:
    def __init__(self, res):
        self.res = res

    def route_table_imports(self):
        result = []
        for route_table in self.res.route_tables.merged:
            result.append(
                f"import {{ routeTable as {route_table.name}RouteTable }}"
                + f" from '{route_table.import_path}';"
            )
        return os.linesep.join(result)


def get_context(self):
    return dict(sections=Sections(self))
