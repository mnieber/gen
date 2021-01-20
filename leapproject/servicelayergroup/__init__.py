from leapdodo.layergroup import create_layer_group
from moonleap import Term, add, tags

from . import layer_configs


@tags(["service:layer-group"])
def create_service_layer_group(term, block):
    layer_group = create_layer_group(Term("server", "layer-group"), block)
    add(layer_group, layer_configs.get(layer_group))
    return layer_group
