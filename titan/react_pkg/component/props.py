import ramda as R


def wrapped_components(self):
    if self.wrapped_child_components:
        return self.wrapped_child_components

    result = []
    for child_component in self.child_components:
        child_result = wrapped_components(child_component)
        if child_result:
            if result:
                raise Exception(
                    f"The {self.name} component has more than one child component "
                    + r"that wraps its children. This is invalid. Please check the spec file"
                )
            result = child_result

    return result


def effect_relations_for_chain(chain):
    effect_terms = []
    for elm in chain:
        effect_terms.extend(elm.side_effects)
    return R.uniq(effect_terms)


def create_router_configs_from_chain(chain):
    from titan.react_pkg.router.resources import concat_router_configs
    from titan.react_state_pkg.state.resources import State

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
