import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    RenderTemplates,
    create_forward,
    extend,
    kebab_to_camel,
    rule,
    tags,
    upper0,
)
from moonleap.verbs import has
from titan.react_state_pkg.state.resources import State

from . import props
from .resources import StateProvider


@tags(["state-provider"])
def create_state_provider(term, block):
    base_name = kebab_to_camel(term.data)
    state_provider = StateProvider(name=f"{upper0(base_name)}StateProvider")
    return state_provider


@rule("state")
def state_created(state):
    return [
        create_forward(state.module, has, f"{state.name}:state-provider"),
        create_forward(state, has, f"{state.name}:state-provider"),
    ]


@extend(State)
class ExtendState:
    state_provider = P.child(has, "state-provider")


@extend(StateProvider)
class ExtendStateProvider(RenderTemplates(__file__)):
    create_router_configs = MemFun(props.create_router_configs)
    p_section_default_props = Prop(props.p_section_default_props)
    state = P.parent(State, has)
