from titan.react_pkg.router_and_module.props import create_component_router_config


def create_router_configs(self):
    return [create_component_router_config(self, url="")]


def _query(graphql_api, item_name):
    queries = graphql_api.queries_that_provide_item_list(item_name)
    if queries:
        return queries[0]
    return None


class Sections:
    def __init__(self, res):
        self.res = res
        self.graphql_api = res.module.react_app.api_module.graphql_api

    def import_query(self):
        query = _query(self.graphql_api, self.res.item_name)
        if query:
            return (
                f"import {{ {query.fun_name} }} from 'src/api/queries/{query.fun_name}"
            )
        return ""

    def run_query(self):
        tab = " " * 8
        query = _query(self.graphql_api, self.res.item_name)
        if query:
            return f"{tab}{query.fun_name}()"
        return ""


def get_context(self):
    return dict(sections=Sections(self))
