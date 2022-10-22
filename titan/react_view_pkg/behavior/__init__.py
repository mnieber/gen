from moonleap import create, empty_rule
from moonleap.verbs import has

from .resources import Behavior

base_tags = {
    "highlight": ["behavior"],
    "selection": ["behavior"],
    "filtering": ["behavior"],
    "deletion": ["behavior"],
}

rules = {
    ("x+item~list", has, "behavior"): empty_rule(),
}


@create("behavior")
def create_behavior(term):
    return Behavior(item_name=term.data, name=term.tag)
