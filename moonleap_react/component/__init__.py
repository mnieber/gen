import moonleap.resource.props as P
from moonleap import Prop, extend, register_add
from moonleap_tools.tool import Tool

from . import props
from .resources import Component, CssImport, JavascriptImport  # noqa


class StoreJavascriptImports:
    javascript_imports = P.tree("has", "javascript-import")


class StoreCssImports:
    css_imports = P.tree("has", "css-import")


@register_add(CssImport)
def add_css_import(resource, css_import):
    resource.css_imports.add(css_import)


@extend(Tool)
class ExtendTool(StoreCssImports):
    pass


@extend(Component)
class ExtendComponent:
    javascript_import_lines = Prop(props.javascript_import_lines)
