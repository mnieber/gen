from jdoc.moonleap.exports import *
from jdoc.titan.widget_reg import *


class BuilderOutput(Entity):
    import_lines: list[str] = []
    react_hooks_lines: list[str] = []
    div_lines: list[str] = []


class Builder(Entity):
    widget_spec: WidgetSpec = None
    output: BuilderOutput = None

    def build(self):
        pass


class ComponentBuilder(Builder):
    pass


class FormBuilder(Builder):
    pass


class DivBuilder(Builder):
    pass


class ComponentBuildFn(Entity):
    pass
