from moonleap.utils.magic_replace import magic_replace
from titan.react_state_pkg.listview.props import get_list_view_route_params
from titan.react_view_pkg.router import RouterConfig


def create_router_configs(self, named_component):
    return [
        RouterConfig(
            component=named_component,
            url="",
            params=get_list_view_route_params(self.item_list.item_name),
        )
    ]


def _query(item_list):
    queries = item_list.provider_queries
    if queries:
        return queries[0]
    return None


effect_args_template = """
type ArgsT = {
    yellowTulip
};
"""


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


def get_context(load_items_effect):
    _ = lambda: None
    _.query = _query(load_items_effect.item_list)
    _.route_params = get_list_view_route_params(load_items_effect.item_list.item_name)

    class Sections:
        def import_query(self):
            if _.query:
                return f"import {{ {_.query.fun_name} }} from 'src/api/queries/{_.query.fun_name}';"
            return ""

        def effect_args(self):
            args = ", ".join(
                [f"{route_param}: string" for route_param in _.route_params]
            )

            return magic_replace(
                effect_args_template,
                [
                    ("yellowTulip", args),
                ],
            )

        def effect_without_args(self):
            if not _.query:
                return (
                    r"# TODO: query that returns a "
                    + f"{load_items_effect.item_list.item_name} not found"
                )

            return f"{_.query.fun_name}()"

        def effect(self):
            if not _.query:
                return (
                    r"# TODO: query that returns a "
                    + f"{load_items_effect.item_list.item_name} not found"
                )

            declare_params = "{ " + ", ".join(_.route_params) + " }"
            use_params = ", ".join(_.route_params)
            extract_params = ", ".join(
                [
                    f"{route_param}: params.{route_param}"
                    for route_param in _.route_params
                ]
            )

            return magic_replace(
                effect_template,
                [
                    ("queryName", _.query.fun_name),
                    ("declare_params", declare_params),
                    ("use_params", use_params),
                    ("extract_params", extract_params),
                ],
            )

    return dict(sections=Sections(), _=_)
