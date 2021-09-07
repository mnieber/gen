from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    StoreTemplateDirs,
    create,
    extend,
    kebab_to_camel,
    register_add,
)
from titan.project_pkg.service import Tool

from . import props
from .resources import Layer, LayerConfig


@register_add(LayerConfig)
def add_layerconfig(resource, layer_config):
    resource.dodo_layer_configs.add(layer_config)


class StoreLayerConfigs:
    dodo_layer_configs = P.tree("p-has", "layer-config")


@create("layer", [])
def create_layer(term, block):
    layer = Layer(name=kebab_to_camel(term.data))
    layer.output_path = ".dodo_commands"
    layer.add_template_dir(Path(__file__).parent / "templates")
    return layer


@extend(Layer)
class ExtendLayer(StoreLayerConfigs, StoreOutputPaths, StoreTemplateDirs):
    get_config = MemFun(props.get_config)


@extend(Tool)
class ExtendTool(StoreLayerConfigs):
    pass
