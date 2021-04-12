import moonleap.resource.props as P
from moonleap import register_add

from .resources import Component, CssImport  # noqa


class StoreCssImports:
    css_imports = P.tree("has", "css-import")


@register_add(CssImport)
def add_css_import(resource, css_import):
    resource.css_imports.add(css_import)
