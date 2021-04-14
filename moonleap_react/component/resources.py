import typing as T
from dataclasses import dataclass, field

from moonleap import title0
from moonleap.resources.outputpath.props import merged_output_path
from moonleap_tools.tool import Tool


@dataclass
class Component(Tool):
    name: str
    react_base_path: str = field(default_factory=lambda: "", init=False)
    dependencies: [T.Any] = field(
        default_factory=lambda: list(), init=False, repr=False
    )

    @property
    def react_tag(self):
        return f"<{title0(self.name)}/>"

    @property
    def import_path(self):
        return self.merged_output_path.relative_to(self.react_base_path)
