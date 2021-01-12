import moonleap.props as props
from moonleap import tags
from moonleap.config import extend

from .localprops import merge_configs
from .resources import Layer


@tags(["layer"])
def create_layer(term, block):
    layer = Layer(name=term.data)
    return layer


def meta():
    from leap_mn.layergroup import LayerGroup

    @extend(Layer)
    class ExtendLayer:
        post_init = True
        templates = "templates"
        output_dir = ".dodo_commands"

        parent_layer_group = props.parent(LayerGroup, "contains", "layer")
        layer_groups = props.children("has", "layer-group")
        config = props.children("has", "layer-config", rdcr=merge_configs)
        layer_configs = props.children("has", "layer-config")

    return [ExtendLayer]
