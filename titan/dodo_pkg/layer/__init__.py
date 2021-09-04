import moonleap.resource.props as P
from moonleap import (
    MemFun,
    RenderTemplates,
    StoreOutputPaths,
    extend,
    kebab_to_camel,
    register_add,
    tags,
)
from titan.project_pkg.service import Tool

from . import props
from .resources import Layer, LayerConfig


@register_add(LayerConfig)
def add_layerconfig(resource, layer_config):
    resource.layer_configs.add(layer_config)


class StoreLayerConfigs:
    layer_configs = P.tree("p-has", "layer-config")


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=kebab_to_camel(term.data))
    layer.output_path = ".dodo_commands"
    return layer


@extend(Layer)
class ExtendLayer(StoreLayerConfigs, StoreOutputPaths, RenderTemplates(__file__)):
    get_config = MemFun(props.get_config)


@extend(Tool)
class ExtendTool(StoreLayerConfigs):
    pass
