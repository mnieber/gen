import os
import typing as T
from dataclasses import dataclass, field

from moonleap.utils.fp import extend_uniq
from moonleap.utils.merge_into_config import merge_into_config

if T.TYPE_CHECKING:
    from titan.react_pkg.component import Component


@dataclass
class BuilderOutput:
    lines: list = field(default_factory=list)
    import_lines: list = field(default_factory=list)
    preamble_lines: list = field(default_factory=list)
    postamble_lines: list = field(default_factory=list)
    external_css_classes: list = field(default_factory=list)
    react_packages_by_module_name: dict = field(default_factory=dict)
    # True if the widget spec or any of its child widget specs has a Children type
    has_children: bool = False
    # All child components needed to render the widget spec
    child_components: T.List["Component"] = field(repr=False, default_factory=list)
    # Additional default properties that are needed for the widget spec
    default_props: T.List[str] = field(repr=False, default_factory=list)

    def add(self, rhs: "BuilderOutput"):
        self.preamble_lines += rhs.preamble_lines
        self.import_lines += rhs.import_lines
        self.lines += rhs.lines
        self.has_children = self.has_children or rhs.has_children
        extend_uniq(self.external_css_classes, rhs.external_css_classes)
        extend_uniq(self.child_components, rhs.child_components)
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

    def clear_lines(self):
        self.lines = []
        self.preable_lines = []
        self.postamble_lines = []
