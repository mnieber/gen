import moonleap.resource.props as P
from moonleap import (MemFun, add, extend, kebab_to_camel, render_templates,
                      rule, tags, title0)
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.module import Module
from moonleap_react_view.router import RouterConfig

from .resources import ListView


@tags(["list-view"])
def create_list_view(term, block):
    name = kebab_to_camel(term.data)
    list_view = ListView(item_name=name, name=f"{name}ListView")
    return list_view


@rule("module", has, "list-view")
def module_has_list_view(module, list_view):
    if not list_view.output_path:
        list_view.output_path = module.output_path
        add(
            list_view,
            RouterConfig(
                url=f"/{module.name}/",
                component_name=f"{title0(list_view.name)}",
                module_name=module.name,
            ),
        )
        module.service.utils_module.add_template_dir(__file__, "templates_utils")

    return service_has_tool_rel(module.service, list_view)


@extend(ListView)
class ExtendListView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "list-view")
