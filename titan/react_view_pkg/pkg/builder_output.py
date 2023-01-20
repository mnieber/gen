import os
import typing as T
from dataclasses import dataclass, field

from moonleap import append_uniq
from moonleap.utils.fp import extend_uniq


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
    # Flags are collected by each builder and passed to the root resource. They
    # can be considered global variables that can be used anywhere to generate code.
    flags: list = field(default_factory=list)

    def merge(self, rhs: "BuilderOutput"):
        self.preamble_hooks_lines += rhs.preamble_hooks_lines
        self.preamble_lines += rhs.preamble_lines
        self.lines += rhs.lines
        self.scss_lines += rhs.scss_lines
        extend_uniq(self.imports_lines, rhs.imports_lines)
        extend_uniq(self.props_lines, rhs.props_lines)
        extend_uniq(self.add_props_lines, rhs.add_props_lines)
        extend_uniq(self.default_props, rhs.default_props)
        extend_uniq(self.flags, rhs.flags)

    def add(
        self,
        lines=None,
        props=None,
        add_props=None,
        default_props=None,
        imports=None,
        scss=None,
        preamble=None,
        preamble_hooks=None,
    ):
        if lines:
            self.lines.extend(lines)
        if props:
            self.props_lines.extend(_trim(props))
        if add_props:
            self.add_props_lines.extend(_trim(add_props))
        if default_props:
            self.default_props.extend(default_props)
        if imports:
            self.imports_lines.extend(imports)
        if scss:
            self.scss_lines.extend(scss)
        if preamble:
            self.preamble_lines.extend(preamble)
        if preamble_hooks:
            self.preamble_hooks_lines.extend(preamble_hooks)

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
        self.merge(rhs)
        return div

    def set_flags(self, flags):
        extend_uniq(self.flags, flags)


def _trim(lines):
    return [x if x == "\n" else x.removesuffix("\n") for x in lines]
