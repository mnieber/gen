from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, extend, kebab_to_camel, rule
from moonleap.verbs import has, posts
from titan.react_pkg.pkg.ml_get import ml_react_app

from .props import get_context
from .resources import FormView

base_tags = [("form-view", ["component"])]


@create("form-view")
def create_form_view(term, block):
    name = kebab_to_camel(term.data)
    form_view = FormView(item_name=name, name=f"{name}FormView")
    form_view.add_template_dir(Path(__file__).parent / "templates", get_context)
    return form_view


@rule("form-view")
def form_view_created(form_view):
    return create_forward(form_view, posts, f"{form_view.item_name}:item")


@rule("module", has, "form-view")
def service_has_forms_module(module, form_view):
    return create_forward(ml_react_app(module), has, "forms:module")


@extend(FormView)
class ExtendFormView:
    item_posted = P.child(posts, "item")
