import moonleap.resource.props as P
from moonleap import extend, kebab_to_camel, rule, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has
from moonleap_project.service import Service, service_has_tool_rel

from .resources import Module  # noqa


@tags(["module"])
def create_module(term, block):
    module = Module(name=kebab_to_camel(term.data))
    module.output_path = f"src/{module.name}"
    return module


@rule("service", has, "module")
def service_has_module(service, module):
    return service_has_tool_rel(service, module)


@extend(Module)
class ExtendModule(StoreTemplateDirs):
    service = P.parent(Service, has, "module")
