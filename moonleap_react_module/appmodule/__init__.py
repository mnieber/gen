import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import Service
from moonleap_react.component import StoreCssImports
from moonleap_tools.tool import Tool

from . import node_package_configs, props
from .render import render_module
from .resources import AppModule  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=term.data)
    module.output_path = f"src/{module.name}"
    add(module, node_package_configs.get())
    return module


@rule("service", has, "module")
def service_has_module(service, module):
    if module.name != "app":
        if service.app_module:
            service.app_module.submodules.add(module)


@extend(Service)
class ExtendService:
    app_module = P.child(has, "app:module")


@extend(AppModule)
class ExtendAppModule(StoreCssImports):
    render = MemFun(render_module)
    css_import_lines = Prop(props.css_import_lines)
    submodules = P.tree(has, "sub-module")
