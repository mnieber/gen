from leapdodo.layer import LayerConfig, create_layer
from moonleap import add, tags

from .layer_configs import get_root_config


@tags(["config:layer"])
def create_config_layer(term, block):
    layer = create_layer(term, block)
    add(layer, LayerConfig(get_root_config()))
    return layer
