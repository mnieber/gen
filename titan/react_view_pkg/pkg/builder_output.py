import os
from dataclasses import dataclass, field

from moonleap.utils.fp import append_uniq


@dataclass
class BuilderOutput:
    is_captured: bool = False
    const_name: str = ""
    lines: list = field(default_factory=list)
    preamble_lines: list = field(default_factory=list)
    postamble_lines: list = field(default_factory=list)
    widget_class_name: str = ""
    components: list = field(default_factory=list)
    external_css_classes: list = field(default_factory=list)
    has_children: bool = False

    def add(self, rhs: "BuilderOutput"):
        self.components += rhs.components
        for css_class in rhs.external_css_classes:
            append_uniq(self.external_css_classes, css_class)

        if rhs.is_captured:
            self.preamble_lines += rhs.div_lines
            self.lines += ["{" + rhs.const_name + "}"]
        else:
            self.preamble_lines += rhs.preamble_lines
            self.lines += rhs.lines

        if rhs.has_children:
            self.has_children = True

    @property
    def debug(self):
        print(self.div)
        return None

    @property
    def div(self):
        return os.linesep.join(self.div_lines)

    @property
    def div_lines(self):
        return (
            self.preamble_lines
            + ["return ("]
            + self.lines
            + [");"]
            + self.postamble_lines
        )
