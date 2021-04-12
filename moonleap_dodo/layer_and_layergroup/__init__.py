import moonleap.resource.props as P
from moonleap import StoreOutputPaths, add_source, extend, rule
from moonleap.verbs import has
from moonleap_dodo.layer import StoreLayerConfigs
from moonleap_dodo.layer.resources import Layer
from moonleap_dodo.layergroup.resources import LayerGroup


@rule("layer", has, "layer-group")
def layer_has_layer_group(layer, layer_group):
    add_source(
        [layer, "layer_configs"],
        layer_group,
        "This layer receives layer configs from a layer-group",
    )


@extend(Layer)
class ExtendLayer(StoreLayerConfigs, StoreOutputPaths):
    parent_layer_group = P.parent(LayerGroup, "contains", "layer")
    layer_groups = P.children(has, "layer-group")
