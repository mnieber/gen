from moonleap_dodo.layer import create_layer
from moonleap import add, tags

from . import layer_configs


@tags(["config:layer"])
def create_config_layer(term, block):
    layer = create_layer(term, block)
    add(layer, layer_configs.get_root_config())
    return layer
