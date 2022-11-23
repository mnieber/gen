import os
from dataclasses import dataclass, field

from moonleap.utils.fp import append_uniq


@dataclass
class BuilderOutput:
    preamble_lines_by_id: dict = field(default_factory=dict)
    postamble_lines_by_id: dict = field(default_factory=dict)
    lines: list = field(default_factory=list)
    widget_class_name: str = ""
    components: list = field(default_factory=list)
    external_css_classes: list = field(default_factory=list)
    has_children: bool = False

    def add(self, rhs: "BuilderOutput"):
        self.components += rhs.components
        for css_class in rhs.external_css_classes:
            append_uniq(self.external_css_classes, css_class)

        _update_lines_by_id(self.preamble_lines_by_id, rhs.preamble_lines_by_id)
        _update_lines_by_id(
            self.postamble_lines_by_id,
            rhs.postamble_lines_by_id,
        )

        self.lines.extend(rhs.lines)
        if rhs.has_children:
            self.has_children = True

    @property
    def preamble(self):
        result = ""
        for id in self.preamble_lines_by_id.keys():
            preamble_lines = self.preamble_lines_by_id[id]
            postamble_lines = self.postamble_lines_by_id[id]
            result += os.linesep.join(preamble_lines + postamble_lines)
        return result

    @property
    def div(self):
        return os.linesep.join(self.lines)


def _update_lines_by_id(lhs, rhs):
    for id, lines in rhs.items():
        target_lines = lhs.setdefault(id, [])
        target_lines.extend(lines)
