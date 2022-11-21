import os
from dataclasses import dataclass, field

from moonleap.utils.fp import append_uniq


@dataclass
class BuilderOutput:
    preamble_lines: list = field(default_factory=list)
    lines: list = field(default_factory=list)
    widget_class_name: str = ""
    components: list = field(default_factory=list)
    external_css_classes: list = field(default_factory=list)
    has_children: bool = False

    def add(self, rhs: "BuilderOutput"):
        self.components += rhs.components
        for css_class in rhs.external_css_classes:
            append_uniq(self.external_css_classes, css_class)
        self.preamble_lines.extend(rhs.preamble_lines)
        self.lines.extend(rhs.lines)
        if rhs.has_children:
            self.has_children = True

    @property
    def div(self):
        return os.linesep.join(self.lines)
