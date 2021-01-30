import moonleap.resource.props as P
from leapproject.service import Service
from leaptools.tool import Tool
from moonleap import MemFun, Prop, add, extend, register_add, rule, tags
from moonleap.verbs import has

from . import node_package_configs, props
from .render import render_module
from .resources import AppModule, CssImport  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=term.data)
    module.output_path = "src"
    add(module, node_package_configs.get())
    return module


@rule("service", has, "app:module")
def service_has_app_module(service, app_module):
    service.add_tool(app_module)


class StoreCssImports:
    css_imports = P.tree("has", "css-import")


@register_add(CssImport)
def add_css_import(resource, css_import):
    resource.css_imports.add(css_import)


@extend(Tool)
class ExtendTool(StoreCssImports):
    pass


@extend(Service)
class ExtendService:
    app_module = P.child(has, "app:module")


@extend(AppModule)
class ExtendAppModule(StoreCssImports):
    render = MemFun(render_module)
    service = P.parent(Service, has, "app:module")
    css_import_lines = Prop(props.css_import_lines)
    submodules = P.tree(has, "sub-module")

    add_submodule = MemFun(props.add_submodule)
