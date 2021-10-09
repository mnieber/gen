from titan.react_state_pkg.state.resources import State
from titan.react_view_pkg.router.resources import concat_router_configs


def create_router_configs_from_chain(chain):

    result = []
    for i in range(len(chain)):
        elm = chain[i]
        if isinstance(elm.obj, State):
            result = concat_router_configs(
                result, elm.obj.state_provider.create_router_configs()
            )
        elif elm.side_effects:
            for rel in elm.side_effects:
                effect = rel.obj
                if effect.tag == "select-item-effect":
                    result = concat_router_configs(
                        result, rel.subj.react_select_effect.create_router_configs()
                    )
                elif effect.tag in ("load-item-effect", "load-items-effect"):
                    result = concat_router_configs(
                        result, rel.subj.react_load_effect.create_router_configs()
                    )

    return result
