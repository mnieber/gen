from moonleap import (
    Prop,
    RenderTemplates,
    create_forward,
    extend,
    kebab_to_camel,
    rule,
    tags,
)
from moonleap.verbs import has

from . import props
from .resources import FormView


@tags(["form-view"])
def create_form_view(term, block):
    name = kebab_to_camel(term.data)
    form_view = FormView(item_name=name + "Form", name=f"{name}FormView")
    return form_view


@rule("module", has, "form-view")
def service_has_forms_module(module, form_view):
    return create_forward(module.react_app, has, "forms:module")


@extend(FormView)
class ExtendFormView(RenderTemplates(__file__)):
    sections = Prop(props.Sections)
