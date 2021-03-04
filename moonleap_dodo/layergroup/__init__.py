import moonleap.resource.props as P
from moonleap import add, extend, kebab_to_camel, tags
from moonleap.verbs import contains
from moonleap_dodo.layer import StoreLayerConfigs

from . import layer_configs
from .resources import LayerGroup


@tags(["layer-group"])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=kebab_to_camel(term.data))
    add(layer_group, layer_configs.get(layer_group))
    return layer_group


@extend(LayerGroup)
class ExtendLayerGroup(StoreLayerConfigs):
    layers = P.children(contains, "layer")
