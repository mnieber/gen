from dataclasses import dataclass

from leaptools.tool import Tool
from moonleap import MemFun, add, extend, rule, tags
from moonleap.verbs import has

from . import node_package_configs
from .render import render_module


@dataclass
class AppModule(Tool):
    name: str


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=term.data)
    module.output_path = "src"
    add(module, node_package_configs.get())
    return module


@rule("service", has, "app:module")
def service_has_app_module(service, app_module):
    service.add_tool(app_module)


@extend(AppModule)
class ExtendModule:
    render = MemFun(render_module)
