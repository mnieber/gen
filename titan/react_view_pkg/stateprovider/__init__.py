from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, empty_rule, extend, kebab_to_camel, u0
from moonleap.blocks.verbs import has, provides

from .resources import StateProvider

base_tags = {"state~provider": ["component"]}


@create("state~provider")
def create_state_provider(term):
    base_name = kebab_to_camel(term.data)
    state_provider = StateProvider(
        base_name=base_name, name=f"{u0(base_name)}StateProvider"
    )
    state_provider.template_dir = Path(__file__).parent / "templates"
    return state_provider


@extend(StateProvider)
class ExtendStateProvider:
    module = P.parent("module", has)
    named_items_provided = P.children(provides, "x+item")
    named_item_lists_provided = P.children(provides, "x+item~list")
    state = P.child(provides, "react-state")


rules = {
    "state~provider": {
        (provides, "react-state"): empty_rule(),
        (provides, "x+item"): empty_rule(),
        (provides, "x+item~list"): empty_rule(),
    },
    "module": {
        (has, "state~provider"): (
            # then the module also has a state
            lambda module, state_provider: create_forward(
                module, has, f"{state_provider.base_name}:state"
            )
        ),
        (has + ("hack",), "state~provider"): (
            #
            lambda module, state_provider: module.renders(
                [state_provider],
                "hooks",
                lambda state_provider: dict(
                    state_provider=state_provider, state=state_provider.state
                ),
                [Path(__file__).parent / "templates_hook"],
            )
        ),
    },
}
