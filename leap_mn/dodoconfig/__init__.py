import json

from leap_mn.layer import Layer, LayerConfig
from moonleap import Resource, reduce, yaml2dict

root_config = """
ROOT:
  src_dir: ${/ROOT/project_dir}/src
  version: 1.0.0
"""


def get_root_config(layer):
    return yaml2dict(root_config)


def create(term, block):
    layer = Layer(name="root")
    layer_config = LayerConfig("root", get_root_config(layer))
    layer.sections.append(layer_config)
    return [layer]


tags = ["dodo-config"]
