from dataclasses import dataclass

from moonleap import Resource


@dataclass
class Layer(Resource):
    name: str

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )
