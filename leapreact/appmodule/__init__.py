import moonleap.resource.props as P
from leapproject.service import Service
from leaptools.tool import Tool
from moonleap import (
    MemFun,
    Prop,
    add,
    extend,
    register_add,
    render_templates,
    rule,
    tags,
)
from moonleap.verbs import has

from . import node_package_configs, props
from .resources import AppModule, CssImport  # noqa


@tags(["app:module"])
def create_app_module(term, block):
    module = AppModule(name=term.data)
    module.output_path = f"src/{module.name}"
    add(module, node_package_configs.get())
    return module


class StoreCssImports:
    css_imports = P.tree("has", "css-import")


@register_add(CssImport)
def add_css_import(resource, css_import):
    resource.css_imports.add(css_import)


@rule("service", has, "module")
def service_has_module(service, module):
    if module.name != "app":
        if service.app_module:
            service.app_module.submodules.add(module)


@extend(Tool)
class ExtendTool(StoreCssImports):
    pass


@extend(Service)
class ExtendService:
    app_module = P.child(has, "app:module")


@extend(AppModule)
class ExtendAppModule(StoreCssImports):
    render = render_templates(__file__)
    css_import_lines = Prop(props.css_import_lines)
    submodules = P.tree(has, "sub-module")
