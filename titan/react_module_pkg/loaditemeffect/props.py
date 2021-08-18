from moonleap.utils.magic_replace import magic_replace
from titan.react_pkg.router_and_module.props import create_component_router_config


def create_router_configs(self):
    return [create_component_router_config(self, url="")]


effect_template = """
    f={(declare_params: ArgsT) => {
        api.getYellowTulip(use_params);
    }}
    getArgs={(params) => {
      return {
        extract_params
      }
    }}
"""


def p_section_effect(self):
    declare_params = "{ " + ", ".join(self.route_params) + " }"
    use_params = ", ".join(self.route_params)
    extract_params = ", ".join(
        [f"{route_param}: params.{route_param}" for route_param in self.route_params]
    )

    return magic_replace(
        effect_template,
        [
            ("yellowTulip", self.item_name + self.name_postfix),
            ("declare_params", declare_params),
            ("use_params", use_params),
            ("extract_params", extract_params),
        ],
    )


effect_args_template = """
type ArgsT = {
    yellowTulip
};
"""


def p_section_effect_args(self):
    args = ", ".join([f"{route_param}: string" for route_param in self.route_params])

    return magic_replace(
        effect_args_template,
        [
            ("yellowTulip", args),
        ],
    )
