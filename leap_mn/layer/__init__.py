import moonleap.props as P
from moonleap import tags
from moonleap.config import extend

from .props import merge_configs
from .resources import Layer


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=term.data)
    return layer


@extend(Layer)
class ExtendLayer:
    post_init = True
    templates = "templates"
    output_dir = ".dodo_commands"

    config = P.children("has", "layer-config", rdcr=merge_configs)
    layer_configs = P.children("has", "layer-config")


def meta():
    return [ExtendLayer]
