import os
import typing as T
from dataclasses import dataclass, field

from moonleap.utils.fp import extend_uniq
from moonleap.utils.merge_into_config import merge_into_config


@dataclass
class BuilderOutput:
    lines: list = field(default_factory=list)
    default_props: T.List[str] = field(repr=False, default_factory=list)
    props_lines: list = field(default_factory=list)
    add_props_lines: list = field(default_factory=list)
    import_lines: list = field(default_factory=list)
    preamble_lines: list = field(default_factory=list)
    postamble_lines: list = field(default_factory=list)
    react_packages_by_module_name: dict = field(default_factory=dict)
    # True if the widget spec or any of its child widget specs has a Children type
    has_children: bool = False

    def add(self, rhs: "BuilderOutput"):
        self.preamble_lines += rhs.preamble_lines
        self.postamble_lines += rhs.postamble_lines
        self.lines += rhs.lines
        self.has_children = self.has_children or rhs.has_children
        extend_uniq(self.import_lines, rhs.import_lines)
        extend_uniq(self.props_lines, rhs.props_lines)
        extend_uniq(self.add_props_lines, rhs.add_props_lines)
        extend_uniq(self.default_props, rhs.default_props)
        merge_into_config(
            self.react_packages_by_module_name, rhs.react_packages_by_module_name
        )

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

    def clear_div_lines(self):
        self.lines = []
        self.preable_lines = []
        self.postamble_lines = []
