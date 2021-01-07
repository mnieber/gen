import json

from leap_mn.layer import Layer, LayerConfig
from moonleap import Resource, tags, yaml2dict


def get_root_config():
    return {
        #
        "src_dir": "${/ROOT/project_dir}/src",
        "version": "1.0.0",
    }


@tags(["dodo-config"])
def create_layer(term, block):
    return [
        Layer(name="config"),
        LayerConfig("root", get_root_config()),
    ]


meta = {}
