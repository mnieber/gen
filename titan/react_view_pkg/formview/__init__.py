from pathlib import Path

from moonleap import create, create_forward, kebab_to_camel, rule
from moonleap.verbs import has

from .props import get_context
from .resources import FormView


@create("form-view", ["component"])
def create_form_view(term, block):
    name = kebab_to_camel(term.data)
    form_view = FormView(item_name=name, name=f"{name}FormView")
    form_view.add_template_dir(Path(__file__).parent / "templates", get_context)
    return form_view


@rule("module", has, "form-view")
def service_has_forms_module(module, form_view):
    return create_forward(module.react_app, has, "forms:module")
