import typing as T
from dataclasses import dataclass, field

from moonleap import Resource, upper0


@dataclass
class Component(Resource):
    name: str
    dependencies: [T.Any] = field(
        default_factory=lambda: list(), init=False, repr=False
    )

    @property
    def react_tag(self):
        return f"<{upper0(self.name)}/>"
