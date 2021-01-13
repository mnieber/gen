import moonleap.props as P
from moonleap import extend, tags

from .props import merge_configs
from .resources import Layer, LayerConfig


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=term.data)
    return layer


class StoreLayerConfigs:
    config = P.children("has", "layer-config", rdcr=merge_configs)
    layer_configs = P.children("has", "layer-config")


@extend(Layer)
class ExtendLayer:
    post_init = True
    templates = "templates"
    output_dir = ".dodo_commands"


extend(Layer)(StoreLayerConfigs)
