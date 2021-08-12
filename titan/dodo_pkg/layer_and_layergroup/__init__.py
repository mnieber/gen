import moonleap.resource.props as P
from moonleap import add_source, extend, rule
from moonleap.verbs import contains, has
from titan.dodo_pkg.layer.resources import Layer
from titan.dodo_pkg.layergroup.resources import LayerGroup


@rule("layer", has, "layer-group")
def layer_has_layer_group(layer, layer_group):
    add_source(
        [layer, "layer_configs"],
        layer_group,
        "This layer receives layer configs from a layer-group",
    )


@extend(Layer)
class ExtendLayer:
    parent_layer_group = P.parent(LayerGroup, contains)
    layer_groups = P.children(has, "layer-group")
