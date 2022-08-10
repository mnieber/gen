import moonleap.resource.props as P
from moonleap import create, create_forward, extend, kebab_to_camel, rule, u0
from moonleap.verbs import has
from titan.react_view_pkg.state.resources import State

from .resources import StateProvider

base_tags = [("state-provider", ["component"])]


@create("state-provider")
def create_state_provider(term):
    base_name = kebab_to_camel(term.data)
    state_provider = StateProvider(name=f"{u0(base_name)}StateProvider")
    return state_provider


@rule("state")
def state_created(state):
    return [
        create_forward(state.module, has, f"{state.meta.term.data}:state-provider"),
        create_forward(state, has, f"{state.meta.term.data}:state-provider"),
    ]


@extend(State)
class ExtendState:
    state_provider = P.child(has, "state-provider", required=True)


@extend(StateProvider)
class ExtendStateProvider:
    state = P.parent("react-state", has, required=True)
