from pathlib import Path

from moonleap import create, kebab_to_camel, u0

from .resources import View

base_tags = {
    "view": ["component", "react-view"],
}


@create("view")
def create_view(term):
    name = u0(kebab_to_camel(term.data + ("view" if term.data.endswith("-") else "")))
    view = View(name=f"{name}")
    view.template_dir = Path(__file__).parent / "templates"

    return view
