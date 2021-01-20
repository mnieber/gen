import moonleap.resource.props as P
from leapdodo.layer import StoreLayerConfigs
from moonleap import add, extend, tags
from moonleap.verbs import contains

from . import layer_configs
from .resources import LayerGroup


@tags(["layer-group"])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=term.data)
    add(layer_group, layer_configs.get(layer_group))
    return layer_group


@extend(LayerGroup)
class ExtendLayerGroup(StoreLayerConfigs):
    layers = P.children(contains, "layer")
