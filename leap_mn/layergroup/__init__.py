from dataclasses import dataclass

import moonleap.props as props
from leap_mn.layer import Layer
from leap_mn.layerconfig import LayerConfig
from moonleap import Resource, rule, tags
from moonleap.config import extend

from .layer_configs import get_layer_config


@dataclass
class LayerGroup(Resource):
    name: str


@tags(["layer-group"])
def create_layer_group(term, block):
    layer_group = LayerGroup(name=term.data)
    layer_group.layer_config = LayerConfig(lambda: get_layer_config(layer_group))
    return layer_group


@rule("layer", "has", "layer-group")
def layer_has_layer_group(layer, layer_group):
    layer.add_to_layer_configs(layer_group.layer_config)


def meta():
    @extend(LayerGroup)
    class ExtendLayerGroup:
        layers = props.children("contains", "layer")

    return [ExtendLayerGroup]
