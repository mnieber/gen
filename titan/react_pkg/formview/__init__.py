
import moonleap.packages.extensions.props as P
from moonleap import create, empty_rule, extend, parts_to_camel, u0
from moonleap.blocks.verbs import saves

from .resources import FormView

base_tags = {
    "form-view": ["component", "react-view"],
}


@create("form-view")
def create_form_view(term):
    name = u0(parts_to_camel(term.parts))
    view = FormView(name=f"{name}")
    return view


@extend(FormView)
class ExtendFormView:
    item = P.child(saves, "item")


rules = {
    "form-view": {(saves, "item"): empty_rule()},
}
