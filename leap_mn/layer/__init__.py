import json

import moonleap.props as props
from leap_mn.service import Service
from moonleap import Resource, tags
from moonleap.props import Prop


class Layer(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Layer name={self.name}"

    @property
    def basename(self):
        return (
            f"{self.parent_layer_group.name}.{self.name}"
            if self.parent_layer_group
            else self.name
        )


@tags(["layer"])
def create_layer(term, block):
    return [Layer(name=term.data)]


def meta():
    from leap_mn.layergroup import LayerGroup
    from leap_mn.project import Project

    return {
        Layer: dict(
            templates="templates",
            output_dir=".dodo_commands",
            props={
                "parent_layer_group": props.parent_of_type(LayerGroup),
                "layer_groups": props.children_of_type(LayerGroup),
            },
        ),
        Service: dict(
            props={
                "layers": props.children_of_type(Layer),
            },
        ),
        Project: dict(
            props={
                "layers": props.children_of_type(Layer),
            },
        ),
    }
