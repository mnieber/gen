from leapdodo.layer import LayerConfig, create_layer
from moonleap import tags

from .layer_configs import get_root_config


@tags(["config:layer"])
def create_config_layer(term, block):
    layer = create_layer(term, block)
    layer.layer_configs.add(LayerConfig(get_root_config()))

    return layer
