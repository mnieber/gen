import moonleap.resource.props as P
from moonleap import add_src, extend
from moonleap.verbs import contains, has
from titan.dodo_pkg.layer.resources import Layer
from titan.dodo_pkg.layergroup.resources import LayerGroup

rules = [(("layer", has, "layer-group"), add_src("dodo_layer_configs"))]


@extend(Layer)
class ExtendLayer:
    parent_layer_group = P.parent(LayerGroup, contains)
    layer_groups = P.children(has, "layer-group")
