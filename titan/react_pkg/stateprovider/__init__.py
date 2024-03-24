import moonleap.extension.props as P
from moonleap import create, create_forward, empty_rule, extend, kebab_to_camel, u0
from moonleap.spec.verbs import has, provides

from .resources import StateProvider

base_tags = {"state~provider": ["component"]}


@create("state~provider")
def create_state_provider(term):
    state_provider = StateProvider(
        name=f"{u0(kebab_to_camel(term.data))}StateProvider",
    )
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
                module, has, f"{state_provider.kebab_data}:state"
            )
        ),
        (has + ("hack",), "state~provider"): empty_rule(),
    },
}
