from pathlib import Path

from moonleap import create, u0
from moonleap.parser.term import term_to_camel

from .resources import View

base_tags = {
    "view": ["component", "react-view"],
}

default_view_templates_dir = Path(__file__).parent / "templates"


@create("view")
def create_view(term):
    name = u0(term_to_camel(term))
    view = View(name=f"{name}")
    view.template_dir = default_view_templates_dir

    return view
