import ramda as R
from moonleap.utils.merge_into_config import merge_into_config

from .resources import SetupFileConfig


def merge(lhs, rhs):
    new_body = dict()
    merge_into_config(new_body, lhs.get_body())
    merge_into_config(new_body, rhs.get_body())
    return SetupFileConfig(new_body)


def p_section_setup_file_config(self):
    configs = list(self.setup_file_configs.merged)
    for tool in self.service.tools:
        configs.extend(tool.setup_file_configs.merged)

    config = R.reduce(merge, SetupFileConfig(body={}), configs)
    result = ""
    for name, body in config.get_body().items():
        result += f"[{name}]\n"
        for k, v in body.items():
            result += f"{k}={v}\n"
    return result
