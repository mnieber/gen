from dataclasses import dataclass

from moonleap import RenderMixin, Resource


@dataclass
class Query(RenderMixin, Resource):
    name: str
