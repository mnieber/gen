import moonleap.resource.props as P
from leapdodo.layer import LayerConfig, StoreLayerConfigs
from moonleap import extend, tags
from moonleap.verbs import contains

from . import layer_configs
from .resources import LayerGroup


@tags(["layer-group"])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=term.data)
    layer_group.layer_configs.add(layer_configs.get(layer_group))
    return layer_group


@extend(LayerGroup)
class ExtendLayerGroup(StoreLayerConfigs):
    layers = P.children(contains, "layer")
