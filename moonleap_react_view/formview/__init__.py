from moonleap import (
    MemFun,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
)
from moonleap.verbs import has

from .resources import FormView


@tags(["form-view"])
def create_form_view(term, block):
    name = kebab_to_camel(term.data)
    form_view = FormView(item_name=name, name=f"{name}FormView")
    return form_view


@rule("module", has, "form-view")
def service_has_forms_module(module, form_view):
    return create_forward(module.service, has, "forms:module")


@extend(FormView)
class ExtendFormView:
    render = MemFun(render_templates(__file__))
