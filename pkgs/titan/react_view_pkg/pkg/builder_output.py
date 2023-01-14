import os
import typing as T
from dataclasses import dataclass, field

from moonleap import append_uniq
from moonleap.utils.fp import extend_uniq
from moonleap.utils.merge_into_config import merge_into_config


@dataclass
class BuilderOutput:
    lines: list = field(default_factory=list)
    default_props: T.List[str] = field(repr=False, default_factory=list)
    props_lines: list = field(default_factory=list)
    add_props_lines: list = field(default_factory=list)
    imports_lines: list = field(default_factory=list)
    scss_lines: list = field(default_factory=list)
    preamble_lines: list = field(default_factory=list)
    preamble_hooks_lines: list = field(default_factory=list)
    flags: list = field(default_factory=list)
    # True if the widget spec or any of its child widget specs has a Children type
    has_children_prop: bool = False
    # True if the widget has no scss file
    no_scss: bool = False

    def add(self, rhs: "BuilderOutput"):
        self.preamble_hooks_lines += rhs.preamble_hooks_lines
        self.preamble_lines += rhs.preamble_lines
        self.lines += rhs.lines
        self.scss_lines += rhs.scss_lines
        self.has_children_prop = self.has_children_prop or rhs.has_children_prop
        self.no_scss = self.no_scss or rhs.no_scss
        extend_uniq(self.imports_lines, rhs.imports_lines)
        extend_uniq(self.props_lines, rhs.props_lines)
        extend_uniq(self.add_props_lines, rhs.add_props_lines)
        extend_uniq(self.default_props, rhs.default_props)
        extend_uniq(self.flags, rhs.flags)

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
            self.preamble_hooks_lines
            + self.preamble_lines
            + ["return ("]
            + self.lines
            + [");"]
        )

    def graft(self, rhs):
        div = rhs.div
        rhs.lines = []
        rhs.preamble_lines = []
        rhs.preamble_hooks_lines = []
        self.add(rhs)
        return div

    def set_flags(self, flags):
        extend_uniq(self.flags, flags)
