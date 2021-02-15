import moonleap.resource.props as P
from moonleap import MemFun, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import Service
from moonleap_react.component import Component

from . import props
from .render import render
from .resources import Module  # noqa


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
    render = MemFun(render)
    service = P.parent(Service, has, "module")

    add_component = MemFun(props.add_component)
