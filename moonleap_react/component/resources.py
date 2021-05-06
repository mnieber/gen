import typing as T
from dataclasses import dataclass, field

from moonleap import Resource, upper0
from moonleap_react.module import Module


@dataclass
class Component(Resource):
    name: str
    module: Module = field(default=None, init=False, compare=False)
    dependencies: [T.Any] = field(
        default_factory=lambda: list(), init=False, repr=False
    )

    @property
    def react_tag(self):
        return f"<{upper0(self.name)}/>"

    @property
    def module_path(self):
        return self.merged_output_path.relative_to(
            self.module.service.merged_output_path
        )
