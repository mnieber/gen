from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, empty_rule, extend, rule, u0
from moonleap.blocks.term import term_to_camel
from moonleap.blocks.verbs import has

from .resources import View

base_tags = {
    "view": ["component", "react-view"],
}

rules = {
    ("view", has, "main+div"): empty_rule(),
}


@create("view")
def create_view(term):
    name = u0(term_to_camel(prefix=term.data, suffix=term.tag))
    view = View(name=f"{name}")
    view.template_dir = Path(__file__).parent / "templates"

    return view


@rule("view")
def created_view(view):
    return create_forward(view, has, "main+:div")


@extend(View)
class ExtendView:
    main_div = P.child(has, "main+div")
