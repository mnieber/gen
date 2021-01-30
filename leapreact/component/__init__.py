import moonleap.resource.props as P
from moonleap import Prop, extend
from moonleap.verbs import has

from . import props
from .resources import Component, JavascriptImport  # noqa


class StoreJavascriptImports:
    javascript_imports = P.tree("has", "javascript-import")


@extend(Component)
class ExtendComponent:
    javascript_import_lines = Prop(props.javascript_import_lines)
