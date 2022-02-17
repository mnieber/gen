import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    create,
    extend,
    feeds,
    kebab_to_camel,
    rule,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has, runs, uses

from . import props
from .resources import Service, Tool
from .tweaks import tweak

rules = [(("service", has + runs, "tool"), feeds("output_paths"))]


@create("service")
def create_service(term):
    service = Service(name=kebab_to_camel(term.data), use_default_config=True)
    service.output_path = service.name + "/"
    return service


@rule("service")
def service_uses_tweaks(service):
    tweak(service)


@extend(Service)
class ExtendService(
    StoreOutputPaths,
    StoreTemplateDirs,
):
    tools = P.children(uses + runs + has, "tool")
    get_tweak_or = MemFun(props.get_tweak_or)


@extend(Tool)
class ExtendTool(StoreOutputPaths, StoreTemplateDirs):
    service = P.parent("service", has + runs, required=True)
