import ramda as R
from moonleap.utils.merge_into_config import merge_into_config

from .resources import LayerConfig


def _merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return LayerConfig(new_body)


def get_config(self):
    return R.reduce(_merge, LayerConfig({}), self.layer_configs.merged)
