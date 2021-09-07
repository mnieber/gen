from moonleap.utils.magic_replace import magic_replace
from titan.react_pkg.router_and_module.props import create_component_router_config


def create_router_configs(self):
    return [create_component_router_config(self, url="")]


def _query(graphql_api, item_name):
    queries = graphql_api.queries_that_provide_item(item_name)
    if queries:
        return queries[0]
    return None


effect_template = """
    f={(declare_params: ArgsT) => {
        queryName(use_params);
    }}
    getArgs={(params) => {
      return {
        extract_params
      }
    }}
"""

effect_args_template = """
type ArgsT = {
    yellowTulip
};
"""


class Sections:
    def __init__(self, res):
        self.res = res
        self.graphql_api = res.module.react_app.api_module.graphql_api

    def effect(self):
        query = _query(self.graphql_api, self.res.item_name)
        if not query:
            return f"# TODO: query that returns a {self.res.item_name} not found"

        declare_params = "{ " + ", ".join(self.res.route_params) + " }"
        use_params = ", ".join(self.res.route_params)
        extract_params = ", ".join(
            [
                f"{route_param}: params.{route_param}"
                for route_param in self.res.route_params
            ]
        )

        return magic_replace(
            effect_template,
            [
                ("queryName", query.fun_name),
                ("declare_params", declare_params),
                ("use_params", use_params),
                ("extract_params", extract_params),
            ],
        )

    def effect_without_args(self):
        query = _query(self.graphql_api, self.res.item_name)
        if not query:
            return f"# TODO: query that returns a {self.res.item_name} not found"

        return f"{query.fun_name}()"

    def effect_args(self):
        args = ", ".join(
            [f"{route_param}: string" for route_param in self.res.route_params]
        )

        return magic_replace(
            effect_args_template,
            [
                ("yellowTulip", args),
            ],
        )

    def import_query(self):
        query = _query(self.graphql_api, self.res.item_name)
        if query:
            return (
                f"import {{ {query.fun_name} }} from 'src/api/queries/{query.fun_name}"
            )
        return ""


def get_context(self):
    return dict(sections=Sections(self))
