from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
    u0,
)
from moonleap.verbs import has, provides

from . import props
from .resources import StateProvider

base_tags = {"state~provider": ["component"]}

rules = {
    ("state~provider", has, "x+pipeline"): empty_rule(),
    ("state~provider", provides, "x+item"): empty_rule(),
    ("state~provider", provides, "x+item~list"): empty_rule(),
}


@create("state~provider")
def create_state_provider(term):
    base_name = kebab_to_camel(term.data)
    state_provider = StateProvider(
        base_name=base_name, name=f"{u0(base_name)}StateProvider"
    )
    state_provider.template_dir = Path(__file__).parent / "templates"
    return state_provider


@rule("state~provider")
def created_state_provider(state_provider):
    return state_provider.load()


@rule("state~provider", provides, "react-state")
def state_provider_provides_state(state_provider, state):
    return [
        create_forward(state_provider.module, has, state),
    ]


@extend(StateProvider)
class ExtendStateProvider:
    module = P.parent("module", has)
    named_items = P.children(provides, "x+item")
    named_item_lists = P.children(provides, "x+item~list")
    pipelines = P.children(has, "x+pipeline")
    state = P.child(provides, "react-state")
    load = MemFun(props.state_provider_load)
