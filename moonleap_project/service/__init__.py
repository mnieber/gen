import moonleap.resource.props as P
from moonleap import (
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
from moonleap_tools.tool import Tool

from .resources import Service
from .tweaks import tweak


@tags(["service"])
def create_service(term, block):
    service = Service(name=kebab_to_camel(term.data), use_default_config=True)
    service.output_path = service.name + "/"
    return service


@rule("service", priority=Priorities.TWEAK.value)
def service_uses_tweaks(service):
    tweak(service)


@rule("service", uses + runs + has, "*", fltr_obj=P.fltr_instance(Tool))
def service_has_tool(service, tool):
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
    src_dir = P.child(has, "src-dir")
