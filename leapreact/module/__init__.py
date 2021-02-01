import moonleap.resource.props as P
from leapproject.service import Service
from leapreact.component import Component
from moonleap import MemFun, extend, register_add, render_templates, rule, tags
from moonleap.verbs import has

from . import props
from .resources import Module


@tags(["module"])
def create_module(term, block):
    module = Module(name=term.data)
    module.output_path = f"src/{module.name}"
    return module


@rule("service", has, "module")
def service_has_module(service, module):
    service.add_tool(module)


@extend(Module)
class ExtendModule:
    render = MemFun(render_templates(__file__))
    service = P.parent(Service, has, "module")

    add_component = MemFun(props.add_component)
