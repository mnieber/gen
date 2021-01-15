import moonleap.props as P
from leap_mn.outputpath import StoreOutputPaths
from moonleap import extend, tags
from moonleap.prop import Prop

from . import props
from .resources import Layer, LayerConfig


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=term.data)
    layer.output_path = ".dodo_commands"
    return layer


class StoreLayerConfigs:
    layer_configs = P.tree(
        "has", "layer-config", merge=props.merge, initial=LayerConfig({})
    )


@extend(Layer)
class ExtendLayer(StoreLayerConfigs, StoreOutputPaths):
    templates = "templates"
