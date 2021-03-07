import moonleap.resource.props as P
from moonleap import (
    MemFun,
    add,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    title0,
)
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.module import Module
from moonleap_react_view.router import RouterConfig

from .resources import FormView


@tags(["form-view"])
def create_form_view(term, block):
    name = kebab_to_camel(term.data)
    form_view = FormView(item_name=name, name=f"{name}FormView")
    return form_view


@rule("module", has, "form-view")
def add_forms_view(module, form_view):
    add(
        form_view,
        RouterConfig(
            url=f"/{module.name}/:{form_view.item_name}Id/edit",
            component_name=title0(form_view.name),
            module_name=module.name,
        ),
    )
    return create_forward(module.service, has, "forms:module")


@rule("module", has, "form-view")
def module_has_form_view(module, form_view):
    form_view.output_path = module.output_path
    return service_has_tool_rel(module.service, form_view)


@extend(FormView)
class ExtendFormView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "form-view")
