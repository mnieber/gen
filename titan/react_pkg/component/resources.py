import typing as T
from dataclasses import dataclass

from moonleap import RenderMixin, Resource, TemplateDirMixin


@dataclass
class Component(TemplateDirMixin, RenderMixin, Resource):
    name: str

    def __post_init__(self):
        self.builder = None
