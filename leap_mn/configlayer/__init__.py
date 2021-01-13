import moonleap.props as P
from leap_mn.layer import Layer, LayerConfig
from leap_mn.project import Project
from moonleap import extend, tags

from .layer_configs import get_root_config


@tags(["config:layer"])
def create_layer(term, block):
    layer = Layer(name="config")
    layer.add_to_layer_configs(LayerConfig(get_root_config()))

    return layer


@extend(Project)
class ExtendProject:
    config_layer = P.child("has", "config:layer", is_doc=False)
