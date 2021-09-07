import moonleap.resource.props as P
from moonleap import add, create, empty_rule, extend, kebab_to_camel
from moonleap.verbs import contains
from titan.dodo_pkg.layer import StoreLayerConfigs

from . import dodo_layer_configs
from .resources import LayerGroup


@create("layer-group", [])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=kebab_to_camel(term.data))
    add(layer_group, dodo_layer_configs.get(layer_group))
    return layer_group


rules = [(("layer-group", contains, "layer"), empty_rule())]


@extend(LayerGroup)
class ExtendLayerGroup(StoreLayerConfigs):
    layers = P.children(contains, "layer")
