from moonleap import Term, add, create
from titan.dodo_pkg.layergroup import create_layer_group

from . import dodo_layer_configs


@create("service:layer-group")
def create_service_layer_group(term, block):
    layer_group = create_layer_group(Term("server", "layer-group"), block)
    add(layer_group, dodo_layer_configs.get(layer_group))
    return layer_group
