import moonleap.resource.props as P
from moonleap import (
    Forward,
    MemFun,
    Rel,
    add,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    title0,
    word_to_term,
)
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

    return service_has_tool_rel(module.service, list_view)


@rule("list-view", has, "behavior")
def create_container(list_view, behavior):
    module = list_view.module
    return create_forward(module, has, f"{module.name}:container")


@rule("list-view", has, "behavior")
def list_view_has_behavior(list_view, behavior):
    return Forward(Rel(list_view.module.term, "has", behavior.term))


@extend(ListView)
class ExtendListView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "list-view")
