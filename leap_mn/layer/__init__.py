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
    def __init__(self, name, body):
        super().__init__()
        self.name = name
        self.body = body

    def __str__(self):
        return f"LayerConfig name={self.name}"

    def get_body(self):
        return self.body(self) if callable(self.body) else self.body

    @property
    def config(self):
        return {self.name.upper(): self.get_body()}


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return LayerConfig(rhs.name, new_body)


def list_of_sections():
    def prop(self):
        items = self.children_of_type(LayerConfig)
        return R.pipe(
            R.always(items),
            R.group_by(R.prop("name")),
            R.values,
            R.map(R.reduce(merge, LayerConfig("acc", {}))),
            R.sort_by(R.prop("name")),
        )(None)

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
                "sections": list_of_sections(),
                "layer_groups": props.children_of_type(LayerGroup),
            },
        ),
        LayerConfig: dict(
            props={
                "layer": props.parent_of_type(Layer),
            },
        ),
    }
