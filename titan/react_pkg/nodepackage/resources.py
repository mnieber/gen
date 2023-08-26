from dataclasses import dataclass

from moonleap import RenderMixin, Resource


@dataclass
class NodePackage(RenderMixin, Resource):
    pass
