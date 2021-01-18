from leapdodo.layer import LayerConfig
from leapdodo.layergroup import create_layer_group
from moonleap import Term, tags

from . import layer_configs as LC


@tags(["service:layer-group"])
def create_service_layer_group(term, block):
    layer_group = create_layer_group(Term("server", "layer-group"), block)
    layer_group.layer_configs.add(LayerConfig(lambda: LC.get_dial_config(layer_group)))
    return layer_group