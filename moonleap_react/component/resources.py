import typing as T
from dataclasses import dataclass, field

from moonleap import Resource, title0
from moonleap_react.module import Module


@dataclass
class Component(Resource):
    name: str
    module: Module = field(init=False, compare=False)
    dependencies: [T.Any] = field(
        default_factory=lambda: list(), init=False, repr=False
    )

    @property
    def react_tag(self):
        return f"<{title0(self.name)}/>"

    @property
    def import_path(self):
        return self.merged_output_path
