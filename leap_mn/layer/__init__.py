import json

from leap_mn.layergroup import LayerGroup
from moonleap import Resource, tags
from yaml import dump


class Layer(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Layer name={self.name}"

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )


class LayerConfig(Resource):
    def __init__(self, name, config):
        super().__init__()
        self.name = name
        self.config = config

    @property
    def as_yaml(self):
        return dump(self.config)


@tags(["layer"])
def create(term, block):
    return [Layer(name=term.data)]


meta = {
    Layer: dict(
        templates="templates",
        parents={"parent_layer_group": LayerGroup},
        children={"sections": [LayerConfig], "layer_groups": [LayerGroup]},
    )
}
