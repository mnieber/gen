from pathlib import Path

import moonleap.resource.props as P
from moonleap import Prop, create, create_forward, extend, kebab_to_camel, rule, u0
from moonleap.verbs import has, provides
from titan.react_pkg.reactmodule import ReactModule
from titan.widgets_pkg.widgetregistry import get_widget_reg

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


@rule("state")
def created_state(state):
    return [
        create_forward(":node-package", has, f"states:node-pkg"),
    ]


@rule("react-app")
def load_states(react_app):
    return props.load_states(get_widget_reg())


@extend(ReactModule)
class ExtendModule:
    states = P.children(has, "state")


@extend(State)
class ExtendState:
    state_provider = P.parent("state~provider", provides)
    ts_var = Prop(props.state_ts_var)
