import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Rel,
    add,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    word_to_term,
)
from moonleap.verbs import has
from moonleap_react.module import Module

from .resources import FormView


@tags(["form-view"])
def create_form_view(term, block):
    name = kebab_to_camel(term.data)
    form_view = FormView(item_name=name, name=f"{name}FormView")
    return form_view


@rule("module", has, "form-view")
def add_forms_module(module, form_view):
    return Rel(module.service.term, has, word_to_term("forms:module"))


@rule("module", has, "form-view")
def module_has_form_view(module, form_view):
    form_view.output_path = module.output_path
    module.service.add_tool(form_view)
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(FormView)
class ExtendFormView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "form-view")


@extend(Module)
class ExtendModule:
    form_views = P.children(has, "form-view")
