import moonleap.resource.props as P
from moonleap import add, extend, rule, title0
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.module import Module
from moonleap_react_view.router import RouterConfig


@rule("module", has, "view")
def module_has_view(module, view):
    view.output_path = module.output_path
    add(
        view,
        RouterConfig(
            url=f"/{module.name}/{view.term.data}/",
            component_name=title0(view.name),
            module_name=module.name,
        ),
    )
    return service_has_tool_rel(module.service, view)


@extend(Module)
class ExtendModule:
    views = P.children(has, "view")
