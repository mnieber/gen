import ramda as R
from moonleap.utils.merge_into_config import merge_into_config

from .resources import SetupFileConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return SetupFileConfig(new_body)


def get_setup_file_config(setup_file):
    configs = list(setup_file.setup_file_configs.merged)
    for tool in setup_file.service.tools:
        configs.extend(tool.setup_file_configs.merged)

    return R.reduce(merge, SetupFileConfig(body={}), configs)
