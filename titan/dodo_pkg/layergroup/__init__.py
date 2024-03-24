import moonleap.extension.props as P
from moonleap import Term, create, empty_rule, extend, kebab_to_camel
from moonleap.spec.verbs import contains, has
from titan.dodo_pkg.layer.resources import DodoLayer

from .resources import DodoLayerGroup


@create("layer-group")
def create_layer_group(term):
    layer_group = DodoLayerGroup(name=kebab_to_camel(term.data))
    return layer_group


@create("service:layer-group")
def create_service_layer_group(term):
    layer_group = create_layer_group(Term(("server", "layer-group")))
    return layer_group


@extend(DodoLayerGroup)
class ExtendDodoLayerGroup:
    layers = P.children(contains, "layer")


@extend(DodoLayer)
class ExtendLayer:
    parent_layer_group = P.parent("layer-group", contains)
    layer_groups = P.children(has, "layer-group")
    service_layer_group = P.child(has, "service:layer-group")


rules = {
    "layer-group": {
        (contains, "layer"): empty_rule()
        #
    },
    "layer": {
        (has, "layer-group"): empty_rule()
        #
    },
}
