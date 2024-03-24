import moonleap.extension.props as P
from moonleap import Prop, create, empty_rule, extend, kebab_to_camel, rule, u0
from moonleap.spec.verbs import has, provides
from titan.react_pkg.reactmodule import ReactModule

from . import props
from .resources import State

base_tags = {"state": ["react-state"]}


@create("state")
def create_state(term):
    prefix = kebab_to_camel(term.data)
    name = u0(prefix + "State")
    state = State(prefix=prefix, name=name)
    return state


@rule("state")
def created_state(state):
    state.module.react_app.set_flags(["app/useStates"])


@extend(ReactModule)
class ExtendModule:
    states = P.children(has, "state")


@extend(State)
class ExtendState:
    state_provider = P.parent("state~provider", provides)
    module = P.parent("react-module", has)
    ts_var = Prop(props.state_ts_var)


rules = {
    "module": {
        (has, "state"): empty_rule(),
    }
}
