import moonleap.props as P
from moonleap import extend, tags

from .props import layer_config_prop
from .resources import Layer, LayerConfig


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=term.data)
    return layer


class StoreLayerConfigs:
    layer_config = layer_config_prop()
    layer_configs = P.children("has", "layer-config")
    layer_config_sources = P.children("has", "layer-config-source")


@extend(Layer)
class ExtendLayer(StoreLayerConfigs):
    templates = "templates"
    output_dir = ".dodo_commands"
