import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend, named, parts_to_camel, u0
from moonleap.blocks.verbs import has

from .resources import Div


@create("x+div")
def create_named_div(term):
    name = u0(parts_to_camel([term.name]))
    named_div = named(Div)()
    named_div.name = name
    named_div.typ = Div(name=name, classnames=[f"'{name}'"])
    return named_div


@extend(named(Div))
class ExtendNamedDiv:
    named_components = P.children(has, "x+component")
    named_divs = P.children(has, "x+div")


rules = {
    "x+div": {
        #
        (has, "x+component"): empty_rule(),
        (has, "x+div"): empty_rule(),
    },
}
