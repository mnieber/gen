import moonleap.props as P
from moonleap import extend, tags
from moonleap.prop import Prop

from .props import merge_configs
from .resources import Layer, LayerConfig


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=term.data)
    return layer


def layer_config_prop():
    def get_value(self):
        return merge_configs(
            self.layer_configs + [x.layer_config for x in self.layer_config_sources]
        )

    return Prop(get_value)


class StoreLayerConfigs:
    layer_config = layer_config_prop()
    layer_configs = P.children("has", "layer-config")
    layer_config_sources = P.children("has", "layer-config-source")


@extend(Layer)
class ExtendLayer(StoreLayerConfigs):
    templates = "templates"
    output_dir = ".dodo_commands"
