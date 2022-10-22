from pathlib import Path

import moonleap.resource.props as P
from moonleap import Prop, create, create_forward, extend, kebab_to_camel, rule, u0
from moonleap.verbs import has, provides
from titan.react_pkg.reactmodule import ReactModule

from . import props
from .resources import State

base_tags = {"state": ["react-state"]}


@create("state")
def create_state(term):
    name = u0(kebab_to_camel(term.data) + "State")
    state = State(name=name)
    return state


@rule("module", has, "state")
def module_renders_state(module, state):
    module.renders(
        [state],
        state.name,
        lambda state: dict(state=state),
        [Path(__file__).parent / "templates"],
    )


@rule("module", has, "react-state")
def module_has_state(module, state):
    state_provider_term = f"{state.meta.term.data}:state~provider"
    return [
        create_forward(module, has, state_provider_term),
        create_forward(state_provider_term, provides, state),
    ]


@rule("state")
def created_state(state):
    return [
        create_forward(":node-package", has, f"states:node-pkg"),
    ]


@extend(ReactModule)
class ExtendModule:
    states = P.children(has, "state")


@extend(State)
class ExtendState:
    state_provider = P.parent("state~provider", provides)
    ts_var = Prop(props.state_ts_var)
