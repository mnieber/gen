import json

from leap_mn.layer import Layer, LayerConfig
from moonleap import Resource, derive, tags, yaml2dict

root_config = """
ROOT:
  src_dir: ${/ROOT/project_dir}/src
  version: 1.0.0
"""


def get_root_config(layer):
    return yaml2dict(root_config)


@tags(["dodo-config"])
def create(term, block):
    return [Layer(name="config")]


@derive(Layer)
def create_root_config(layer):
    if layer.name == "config":
        return [LayerConfig("root", get_root_config(layer))]
    return []
