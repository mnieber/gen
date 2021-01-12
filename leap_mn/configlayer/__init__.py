import moonleap.props as props
from leap_mn.layer import Layer
from leap_mn.layerconfig import LayerConfig
from moonleap import extend, tags

from .layer_configs import get_root_config


@tags(["config:layer"])
def create_layer(term, block):
    layer = Layer(name="config")
    layer.add_to_layer_configs(LayerConfig(get_root_config()))

    return layer


def meta():
    from leap_mn.project import Project

    @extend(Project)
    class ExtendProject:
        config_layer = props.child("has", "config:layer")

    return [ExtendProject]
