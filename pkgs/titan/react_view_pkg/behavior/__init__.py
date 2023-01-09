from moonleap import create, empty_rule, kebab_to_camel, named
from moonleap.blocks.verbs import has

from .resources import Behavior

base_tags = {
    "behavior": ["react-prop"],
    "deletion": ["behavior"],
    "drag-and-drop": ["behavior"],
    "editing": ["behavior"],
    "filtering": ["behavior"],
    "highlight": ["behavior"],
    "insertion": ["behavior"],
    "selection": ["behavior"],
}

rules = {
    ("x+item~list", has, "behavior"): empty_rule(),
}


@create("behavior")
def create_behavior(term):
    has_param = term.tag in ("selection", "filtering", "highlight", "insertion")
    return Behavior(
        item_name=kebab_to_camel(term.data),
        name=kebab_to_camel(term.tag),
        has_param=has_param,
    )


@create("x+x:behavior")
def create_named_behavior(term):
    return named(Behavior)()
