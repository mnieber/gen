import json

from leap_mn.layer import Layer
from leap_mn.layerconfig import LayerConfig
from moonleap import Resource, tags, yaml2dict


def get_root_config():
    return dict(
        command_path=["~/.dodo_commands/default_project/commands/*"],
        src_dir="${/ROOT/project_dir}/src",
        shared_config_dir=r"${/ROOT/src_dir}/extra/.dodo_commands",
        version="1.0.0",
    )


@tags(["dodo-config"])
def create_layer(term, block):
    return [
        Layer(name="config"),
        LayerConfig(dict(ROOT=get_root_config())),
    ]


meta = {}
