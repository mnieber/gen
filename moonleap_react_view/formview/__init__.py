import moonleap.resource.props as P
from moonleap import MemFun, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_react.module import Module

from .resources import FormView


@tags(["form-view"])
def create_form_view(term, block):
    name = term.data
    form_view = FormView(item_name=name, name=f"{name}FormView", import_path="")
    return form_view


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
