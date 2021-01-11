import json

import moonleap.props as props
import moonleap.rules as rules
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
    layer = Layer(name="config")
    layer.add_child(LayerConfig(dict(ROOT=get_root_config())))

    return layer


def add_dodo_config_to_project(project, dodo_config):
    project.add_child(dodo_config)


meta = {}

rules = {
    "project": {("has", "dodo-config"): rules.add_child},
}
