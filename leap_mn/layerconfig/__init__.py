import moonleap.props as props
import ramda as R
from moonleap.config import extend
from moonleap.utils.merge_into_config import merge_into_config

from .resources import LayerConfig


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
