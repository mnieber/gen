import json

from leap_mn.layergroup import LayerGroup
from moonleap import Resource
from yaml import dump


class Layer(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.layer_groups = []
        self.sections = []
        self.src_dir = None

    @property
    def parent_layer_group(self):
        return self.parent(LayerGroup)

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )

    def describe(self):
        return dict(
            name=self.name,
            layer_groups=[x.name for x in self.layer_groups],
            sections=[x.name for x in self.sections],
            src_dir=self.src_dir.location if self.src_dir else None,
        )


class LayerConfig(Resource):
    def __init__(self, name, config):
        super().__init__()
        self.name = name
        self.config = config

    @property
    def as_yaml(self):
        return dump(self.config)

    def describe(self):
        return dict(name=self.name)


def create(term, block):
    return [Layer(name=term.data)]


tags = ["layer"]

templates_by_resource_type = [(Layer, "templates")]
