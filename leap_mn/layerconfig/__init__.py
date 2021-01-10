import moonleap.props as props
import ramda as R
from leap_mn.layer import Layer
from moonleap import Resource
from moonleap.props import Prop
from moonleap.utils import merge_into_config
from moonleap.utils.uppercase_dict_keys import uppercase_dict_keys


class LayerConfig(Resource):
    def __init__(self, body):
        super().__init__()
        self.body = body

    def __str__(self):
        return f"LayerConfig name={self.name}"

    @property
    def name(self):
        return "/".join(self.get_body().keys())

    def get_body(self):
        body = self.body(self) if callable(self.body) else self.body
        return uppercase_dict_keys(body)


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return LayerConfig(new_body)


def get_merged_layer_config():
    def prop(self):
        configs = self.children_of_type(LayerConfig)
        merged = R.reduce(merge, LayerConfig({}), configs)
        return LayerConfig(merged.get_body())

    return Prop(prop, child_resource_type=LayerConfig)


def meta():
    return {
        Layer: dict(
            props={
                "config": get_merged_layer_config(),
            },
        ),
    }
