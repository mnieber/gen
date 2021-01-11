import typing as T
from dataclasses import dataclass

import moonleap.props as props
import ramda as R
from moonleap import Resource
from moonleap.config import extend
from moonleap.utils.merge_into_config import merge_into_config
from moonleap.utils.uppercase_dict_keys import uppercase_dict_keys


@dataclass
class LayerConfig(Resource):
    body: T.Union[dict, T.Callable]

    def __repr__(self):
        return f"LayerConfig name={self.name}"

    @property
    def name(self):
        return "/".join(self.get_body().keys())

    def get_body(self):
        body = self.body() if callable(self.body) else self.body
        return uppercase_dict_keys(body)


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return LayerConfig(new_body)


def merge_configs(configs):
    merged = R.reduce(merge, LayerConfig({}), configs)
    return LayerConfig(merged.get_body())


def meta():
    from leap_mn.layer import Layer

    @extend(Layer)
    class ExtendLayer:
        config = props.children("has", "layer-config", rdcr=merge_configs)
        layer_configs = props.children("has", "layer-config")

    return [ExtendLayer]
