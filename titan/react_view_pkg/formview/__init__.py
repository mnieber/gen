from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
    u0,
)
from moonleap.verbs import has, posts
from titan.react_pkg.pkg.ml_get import ml_react_app

from .props import get_context
from .resources import FormView

base_tags = [("form-view", ["component"])]
rules = [(("form-view", posts, "item"), empty_rule())]


@create("form-view")
def create_form_view(term):
    name = f"{u0(kebab_to_camel(term.data))}FormView"
    form_view = FormView(name=name)
    form_view.add_template_dir(Path(__file__).parent / "templates", get_context)
    return form_view


@rule("module", has, "form-view")
def service_has_forms_module(module, form_view):
    return create_forward(ml_react_app(module), has, "forms:module")


@extend(FormView)
class ExtendFormView:
    item_posted = P.child(posts, "item")
    item_name = Prop(props.item_name)
    create_router_configs = MemFun(props.create_router_configs)
