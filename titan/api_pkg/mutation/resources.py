from dataclasses import dataclass

from moonleap import RenderMixin, Resource


@dataclass
class Mutation(RenderMixin, Resource):
    name: str
