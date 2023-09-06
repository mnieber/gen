import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend, named, u0
from moonleap.blocks.term import term_to_camel
from moonleap.blocks.verbs import has

from .resources import Div

rules = {
    ("div", has, "component"): empty_rule(),
}


@create("x+div")
def create_named_div(term):
    named_div = named(Div)()
    named_div.name = u0(term_to_camel(prefix=term.name, suffix=term.tag))
    named_div.type = Div()
    return named_div


@extend(named(Div))
class ExtendNamedDiv:
    components = P.children(has, "component")
    divs = P.children(has, "x+div")
