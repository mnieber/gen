from dataclasses import dataclass

from moonleap import RenderMixin, Resource, TemplateDirMixin


@dataclass
class ReactModule(TemplateDirMixin, RenderMixin, Resource):
    name: str
