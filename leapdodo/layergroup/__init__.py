import moonleap.resource.props as P
from leapdodo.layer import LayerConfig, StoreLayerConfigs
from moonleap import extend, tags

from . import layer_configs as LC
from .resources import LayerGroup


@tags(["layer-group"])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=term.data)
    layer_group.layer_configs.add(
        LayerConfig(lambda: LC.get_group_layer_config(layer_group))
    )
    return layer_group


@extend(LayerGroup)
class ExtendLayerGroup(StoreLayerConfigs):
    layers = P.children("contains", "layer")
