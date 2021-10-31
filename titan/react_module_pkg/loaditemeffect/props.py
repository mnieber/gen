from moonleap.utils.inflect import plural
from moonleap.utils.join import join
from moonleap.utils.magic_replace import magic_replace
from titan.react_state_pkg.itemview.props import get_item_view_route_params
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)


def create_router_configs(self):
    route_params = get_item_view_route_params(self.item.item_name)
    postfix = join(prefix="/:", infix="/:".join(route_params))
    url = f"{plural(self.item.item_name)}{postfix}"

    return [create_component_router_config(self, url="")]


def _query(item):
    queries = item.provider_queries
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


def get_context(load_item_effect):
    _ = lambda: None
    _.query = _query(load_item_effect.item)
    _.route_params = get_item_view_route_params(load_item_effect.item.item_name)

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
                return f"# TODO: query that returns a {load_item_effect.item.item_name} not found"

            return f"{_.query.fun_name}()"

        def effect(self):
            if not _.query:
                return f"# TODO: query that returns a {load_item_effect.item.item_name} not found"

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
