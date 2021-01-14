import ramda as R
from moonleap.utils.merge_into_config import merge_into_config

from .resources import LayerConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return LayerConfig(new_body)


def merge_configs(configs):
    return R.reduce(merge, LayerConfig({}), configs)


def layer_config(self):
    return merge_configs(
        self.layer_configs + [x.layer_config for x in self.layer_config_sources]
    )
