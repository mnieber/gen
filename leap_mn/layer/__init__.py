import moonleap.props as P
from moonleap import extend, tags
from moonleap.prop import Prop

from . import props
from .resources import Layer, LayerConfig


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=term.data)
    return layer


class StoreLayerConfigs:
    layer_config = Prop(props.layer_config)
    layer_configs = P.children("has", "layer-config")
    layer_config_sources = P.children("has", "layer-config-source")


@extend(Layer)
class ExtendLayer(StoreLayerConfigs):
    templates = "templates"
    output_dir = ".dodo_commands"
