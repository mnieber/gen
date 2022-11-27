from pathlib import Path

from moonleap import create, u0

from .resources import View

base_tags = {
    "view": ["component", "react-view"],
}


@create("view")
def create_view(term):
    name = u0(term.to_camel())
    view = View(name=f"{name}")
    view.template_dir = Path(__file__).parent / "templates"

    return view
