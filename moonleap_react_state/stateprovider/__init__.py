import moonleap.resource.props as P
from moonleap import (
    MemFun,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    upper0,
)
from moonleap.utils.inflect import singular
from moonleap.verbs import has
from moonleap_react_state.state.resources import State

from . import props
from .resources import StateProvider


@tags(["state-provider"])
def create_state_provider(term, block):
    kebab_name = term.data
    items_name = kebab_to_camel(kebab_name)
    item_name = singular(items_name)
    state_provider = StateProvider(
        name=f"{upper0(items_name)}CtrProvider", item_name=item_name
    )
    return state_provider


@rule("state")
def state_created(state):
    return create_forward(state, has, f"{state.name}:state-provider")


@rule("state", has, "state-provider")
def state_has_state_provider(state, state_provider):
    state_provider.output_paths.add_source(state)


@extend(State)
class ExtendState:
    state_provider = P.child(has, "state-provider")


@extend(StateProvider)
class ExtendStateProvider:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)