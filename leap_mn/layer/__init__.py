from dataclasses import dataclass

import moonleap.props as props
from moonleap import Resource, tags
from moonleap.config import extend


@dataclass
class Layer(Resource):
    name: str

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )


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

    return [ExtendLayer]
