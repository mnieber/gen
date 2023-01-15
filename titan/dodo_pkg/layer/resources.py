from dataclasses import dataclass

from moonleap import RenderMixin, Resource


@dataclass
class DodoLayer(RenderMixin, Resource):
    name: str
    is_root: bool

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )
