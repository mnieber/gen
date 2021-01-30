import moonleap.resource.props as P
from leapproject.service import Service
from moonleap import MemFun, extend, rule, tags
from moonleap.verbs import has

from .render import render_module
from .resources import Module


@tags(["module"])
def create_module(term, block):
    module = Module(name=term.data)
    module.output_path = f"src/{module.name}"
    return module


@rule("service", has, "module")
def service_has_module(service, module):
    module.output_paths.add_source(service)
    service.add_tool(module)


@extend(Module)
class ExtendModule:
    render = MemFun(render_module)
    service = P.parent(Service, has, "module")
