import moonleap.props as P
from leap_mn.layer import Layer
from leap_mn.layerconfig import LayerConfig
from moonleap import extend, rule, tags

from .layer_configs import get_layer_config
from .resources import LayerGroup


@tags(["layer-group"])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=term.data)
    layer_group.layer_config = LayerConfig(lambda: get_layer_config(layer_group))
    return layer_group


@rule("layer", "has", "layer-group")
def layer_has_layer_group(layer, layer_group):
    layer.add_to_layer_configs(layer_group.layer_config)


@extend(LayerGroup)
class ExtendLayerGroup:
    layers = P.children("contains", "layer")


@extend(Layer)
class ExtendLayer:
    parent_layer_group = P.parent(LayerGroup, "contains", "layer")
    layer_groups = P.children("has", "layer-group")


def meta():
    return [ExtendLayerGroup, ExtendLayer]
