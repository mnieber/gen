from moonleap import MemFun, Prop, create_forward, extend, kebab_to_camel, rule, tags
from moonleap.verbs import provides

from . import props
from .resources import SelectionBvr


@tags(["selection"])
def create_behavior(term, block):
    item_name = kebab_to_camel(term.data)
    behavior = SelectionBvr(item_name=item_name, name=term.tag)
    return behavior


@rule("state", provides, "selection")
def state_provides_selection(state, selection):
    return create_forward(state, provides, f"{selection.item_name}:highlight")


@extend(SelectionBvr)
class ExtendSelectionBvr:
    p_section_imports = Prop(props.p_section_imports)
    p_section_callbacks = MemFun(props.p_section_callbacks)
    p_section_declare_policies = MemFun(props.p_section_declare_policies)
    p_section_policies = MemFun(props.p_section_policies)
    p_section_default_props = MemFun(props.p_section_default_props)
