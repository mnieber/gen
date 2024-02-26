
import moonleap.packages.extensions.props as P
from moonleap import (
    Priorities,
    create,
    create_forward,
    empty_rule,
    extend,
    parts_to_camel,
    u0,
)
from moonleap.blocks.verbs import has

from .resources import View

base_tags = {
    "view": ["component", "react-view"],
}


@create("view")
def create_view(term):
    name = u0(parts_to_camel(term.parts))
    view = View(name=f"{name}")
    return view


def component_is_in_a_module(view, named_component):
    if not named_component.typ.module:
        return create_forward(view.module, has, named_component.typ)


@extend(View)
class ExtendView:
    named_components = P.children(has, "x+component")
    named_divs = P.children(has, "x+div")


rules = {
    "view": {
        (has, "x+component", Priorities.LOW.value): (
            #
            component_is_in_a_module
        ),
        (has, "x+div"): empty_rule(),
    },
}
