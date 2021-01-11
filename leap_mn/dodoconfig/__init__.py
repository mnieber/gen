import moonleap.props as props
from leap_mn.layer import Layer
from leap_mn.layerconfig import LayerConfig
from moonleap import extend, tags


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
    layer.add_to_layer_configs(LayerConfig(dict(ROOT=get_root_config())))

    return layer


def meta():
    from leap_mn.project import Project

    @extend(Project)
    class ExtendProject:
        config_layer = props.child("has", "dodo-config")

    return [ExtendProject]
