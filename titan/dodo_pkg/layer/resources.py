from dataclasses import dataclass

from moonleap import Resource


@dataclass
class DodoLayer(Resource):
    name: str
    is_root: bool

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )
