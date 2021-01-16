import moonleap.resource.props as P
from leap_mn.layer import Layer, LayerConfig, StoreLayerConfigs
from moonleap import extend, rule, tags

from . import layer_configs as LC
from .resources import LayerGroup


@tags(["layer-group"])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=term.data)
    layer_group.layer_configs.add(
        LayerConfig(lambda: LC.get_group_layer_config(layer_group))
    )
    return layer_group


@rule("layer", "has", "layer-group")
def layer_has_layer_group(layer, layer_group):
    layer.layer_configs.add_source(layer_group)


@extend(LayerGroup)
class ExtendLayerGroup(StoreLayerConfigs):
    layers = P.children("contains", "layer")


@extend(Layer)
class ExtendLayer:
    parent_layer_group = P.parent(LayerGroup, "contains", "layer")
    layer_groups = P.children("has", "layer-group")
