from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
    u0,
)
from moonleap.verbs import has, runs

from .resources import FormView

base_tags = {"form-view": ["component"]}
rules = {("form-view", runs, "mutation"): empty_rule()}


@create("form-view")
def create_form_view(term):
    name = f"{u0(kebab_to_camel(term.data))}FormView"
    form_view = FormView(name=name)
    form_view.template_dir = Path(__file__).parent / "templates"
    return form_view


@rule("module", has, "form-view")
def service_has_forms_module(module, form_view):
    return create_forward(module.react_app, has, "forms:module")


@extend(FormView)
class ExtendFormView:
    mutation = P.child(runs, "mutation")
