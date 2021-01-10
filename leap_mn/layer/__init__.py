import json

import moonleap.props as props
import ramda as R
from moonleap import Resource, tags
from moonleap.props import Prop
from moonleap.utils import merge_into_config


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


class LayerConfig(Resource):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def __str__(self):
        return f"LayerConfig name={self.name}"

    @property
    def name(self):
        layers = self.parents_of_type(Layer)
        return layers[0].name if len(layers) == 1 else ""

    def get_body(self):
        body = self.body(self) if callable(self.body) else self.body
        return R.pipe(
            R.always(body),
            R.to_pairs,
            R.map(lambda x: (x[0].upper(), x[1])),
            R.sort_by(lambda x: x[0]),
            R.from_pairs,
        )(None)


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return LayerConfig(new_body)


def get_config():
    def prop(self):
        configs = self.children_of_type(LayerConfig)
        merged = R.reduce(merge, LayerConfig({}), configs)
        return merged.get_body()

    return Prop(prop, child_resource_type=LayerConfig)


@tags(["layer"])
def create_layer(term, block):
    return [Layer(name=term.data)]


def meta():
    from leap_mn.layergroup import LayerGroup

    return {
        Layer: dict(
            templates="templates",
            output_dir=".dodo_commands",
            props={
                "parent_layer_group": props.parent_of_type(LayerGroup),
                "config": get_config(),
                "layer_groups": props.children_of_type(LayerGroup),
            },
        ),
        LayerConfig: dict(
            props={
                "layer": props.parent_of_type(Layer),
            },
        ),
    }
