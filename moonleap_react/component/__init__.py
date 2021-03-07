import moonleap.resource.props as P
from moonleap import extend, register_add
from moonleap_tools.tool import Tool

from .resources import Component, CssImport  # noqa


class StoreCssImports:
    css_imports = P.tree("has", "css-import")


@register_add(CssImport)
def add_css_import(resource, css_import):
    resource.css_imports.add(css_import)


@extend(Tool)
class ExtendTool(StoreCssImports):
    pass
