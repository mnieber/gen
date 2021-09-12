from titan.dodo_pkg.layer import create_layer
from moonleap import add, create

from . import dodo_layer_configs


@create(["config:layer"])
def create_config_layer(term, block):
    layer = create_layer(term, block)
    add(layer, dodo_layer_configs.get_root_config())
    return layer
