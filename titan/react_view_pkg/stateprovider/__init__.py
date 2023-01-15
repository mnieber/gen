import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend, kebab_to_camel, rule, u0
from moonleap.blocks.verbs import has, provides
from titan.react_view_pkg.view import default_view_templates_dir

from . import props
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
    state_provider.template_dir = default_view_templates_dir
    return state_provider


@rule("state~provider")
def created_state_provider(state_provider):
    return props.state_provider_load(state_provider)


@extend(StateProvider)
class ExtendStateProvider:
    module = P.parent("module", has)
    named_items_provided = P.children(provides, "x+item")
    named_item_lists_provided = P.children(provides, "x+item~list")
    state = P.child(provides, "react-state")
