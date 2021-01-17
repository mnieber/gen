from moonleap.utils.merge_into_config import merge_into_config

from .resources import SetupFileConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return SetupFileConfig(new_body)
