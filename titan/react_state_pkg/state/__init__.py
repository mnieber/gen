from pathlib import Path

import moonleap.resource.props as P
from moonleap import Prop, add, create, empty_rule, extend, kebab_to_camel, named, rule
from moonleap.verbs import has
from titan.api_pkg.pipeline.resources import Pipeline
from titan.react_pkg.module import Module
from titan.react_pkg.nodepackage import load_node_package_config
from titan.react_pkg.pkg.ml_get import ml_react_app

from . import react_app_configs
from .props import get_context
from .resources import State

base_tags = [("state", ["component", "react-state"])]

rules = [
    (("state", has, "x+pipeline"), empty_rule()),
]


@create("state")
def create_state(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    state = State(name=name)
    state.add_template_dir(
        Path(__file__).parent / "templates",
        get_context,
        # If the state has no behaviors, then the state provider will
        # provide resources directly from its inputs.
        skip_render=lambda x: not x.has_bvrs,
    )
    add(state, load_node_package_config(__file__))
    return state


@rule("module", has, "state")
def module_has_state(module, state):
    react_app = ml_react_app(module)
    add(react_app, react_app_configs.config)


@extend(Module)
class ExtendModule:
    states = P.children(has, "state")


@extend(State)
class ExtendState:
    module = P.parent("module", has)
    pipelines = P.children(has, "x+pipeline")
    has_bvrs = Prop(props.has_bvrs)


@extend(named(Pipeline))
class ExtendNamedPipeline:
    state = P.parent("react-state", has)
