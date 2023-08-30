from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import (
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
    u0,
)
from moonleap.blocks.verbs import has, provides

from .resources import StateProvider

base_tags = {"state~provider": ["component"]}

rules = {
    ("state~provider", provides, "react-state"): empty_rule(),
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


@rule("module", has, "state~provider")
def module_renders_state_provider(module, state_provider):
    module.renders(
        [state_provider],
        "hooks",
        lambda state_provider: dict(
            state_provider=state_provider, state=state_provider.state
        ),
        [Path(__file__).parent / "templates_hook"],
    )


@rule("module", has, "state~provider")
def module_has_state(module, state_provider):
    state_term = f"{state_provider.base_name}:state"
    return create_forward(module, has, state_term)


@extend(StateProvider)
class ExtendStateProvider:
    module = P.parent("module", has)
    named_items_provided = P.children(provides, "x+item")
    named_item_lists_provided = P.children(provides, "x+item~list")
    state = P.child(provides, "react-state")
