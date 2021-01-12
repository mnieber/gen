import ramda as R
from leap_mn.layerconfig import LayerConfig
from moonleap.utils.merge_into_config import merge_into_config


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return LayerConfig(new_body)


def merge_configs(configs):
    merged = R.reduce(merge, LayerConfig({}), configs)
    return LayerConfig(merged.get_body())
