import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Priorities,
    StoreOutputPaths,
    create_forward,
    extend,
    kebab_to_camel,
    rule,
    tags,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has, runs, uses

from . import props
from .resources import Service, Tool
from .tweaks import tweak


@tags(["service"])
def create_service(term, block):
    service = Service(name=kebab_to_camel(term.data), use_default_config=True)
    service.output_path = service.name + "/"
    return service


@rule("service", priority=Priorities.TWEAK.value)
def service_uses_tweaks(service):
    tweak(service)


@rule("service", has, "tool")
def service_has_tool(service, tool):
    tool.output_paths.add_source(service)


@rule("service", uses + runs + has, "*", fltr_obj=P.fltr_instance(Tool))
def service_has_tool_instance(service, tool):
    return create_forward(
        service,
        has,
        ":tool",
        obj_res=tool,
    )


@extend(Service)
class ExtendService(
    StoreOutputPaths,
    StoreTemplateDirs,
):
    tools = P.children(has, "tool")
    get_tweak_or = MemFun(props.get_tweak_or)


@extend(Tool)
class ExtendTool(StoreOutputPaths):
    service = P.parent(Service, has + runs)
