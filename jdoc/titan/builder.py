import typing as T

from jdoc.moonleap.exports import *
from jdoc.titan.widget_reg import *


class BuilderOutput(Entity):
    import_lines: T.List[str] = []
    react_hooks_lines: T.List[str] = []
    div_lines: T.List[str] = []


class Builder(Entity):
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
