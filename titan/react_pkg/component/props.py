import ramda as R
from moonleap.utils.fp import uniq


def wrapped_components(self):
    if self.wrapped_child_components:
        return self.wrapped_child_components

    result = []
    for child_component in self.typ.child_components:
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
    return uniq(effect_terms)
