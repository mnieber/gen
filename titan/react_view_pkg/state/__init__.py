from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    named,
    rule,
)
from moonleap.verbs import has
from titan.api_pkg.pipeline.resources import Pipeline
from titan.react_pkg.reactmodule import ReactModule

from . import props
from .resources import State

base_tags = [("state", ["component", "react-state"])]

rules = [
    (("state", has, "x+pipeline"), empty_rule()),
    (("module", has, "state"), empty_rule()),
]


@create("state")
def create_state(term):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    state = State(name=name)
    state.template_dir = Path(__file__).parent / "templates"
    return state


@rule("state")
def created_state(state):
    return create_forward(":node-package", has, f"states:node-pkg")


@extend(ReactModule)
class ExtendModule:
    states = P.children(has, "state")


@extend(State)
class ExtendState:
    module = P.parent("module", has)
    pipelines = P.children(has, "x+pipeline")
    has_bvrs = Prop(props.has_bvrs)
    ts_var = Prop(props.state_ts_var)


@extend(named(Pipeline))
class ExtendNamedPipeline:
    state = P.parent("react-state", has)
