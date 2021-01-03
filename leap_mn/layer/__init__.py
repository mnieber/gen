import json

from moonleap import Resource, reduce
from yaml import dump


class Layer(Resource):
    def __init__(self, name):
        self.name = name
        self.group_name = None
        self.is_root = name == "root"
        self.layer_groups = []
        self.sections = []
        self.src_dir = None

    @property
    def full_name(self):
        return f"{self.group_name}.{self.name}" if self.group_name else self.name

    def describe(self):
        return dict(
            name=self.full_name,
            layer_groups=[x.name for x in self.layer_groups],
            sections=[x.name for x in self.sections],
            src_dir=self.src_dir.location if self.src_dir else None,
        )


class LayerConfig(Resource):
    def __init__(self, name, config):
        self.name = name
        self.config = config

    @property
    def as_yaml(self):
        return dump(self.config)

    def describe(self):
        return dict(name=self.name)


def create(term, block):
    return [Layer(name=term.data)]


@reduce(a_resource="leap_mn.Layer", b_resource=LayerConfig)
def add_config(layer, layer_config):
    if layer_config.is_created_in_block_that_mentions(layer):
        layer.sections.append(layer_config)


@reduce(a_resource=Layer, b_resource="leap_mn.LayerGroup")
def add_layer_group(layer, layer_group):
    if layer.is_root:
        layer.layer_groups.append(layer_group)


@reduce(a_resource=Layer, b_resource="leap_mn.SrcDir")
def add_src_dir(layer, src_dir):
    if layer.is_root:
        layer.src_dir = src_dir


tags = ["layer"]

templates_by_resource_type = [(Layer, "templates")]
