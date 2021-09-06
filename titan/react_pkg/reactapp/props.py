import os

from moonleap.utils.merge_into_config import merge_into_config
from titan.react_pkg.reactapp.resources import ReactAppConfig


def _merge(lhs, rhs):
    result = ReactAppConfig()
    result.flags = {}
    merge_into_config(result.flags, lhs.flags)
    merge_into_config(result.flags, rhs.flags)
    result.index_imports = lhs.index_imports + os.linesep + rhs.index_imports
    result.index_body = lhs.index_body + os.linesep + rhs.index_body
    return result


def get_config(react_app) -> ReactAppConfig:
    result = ReactAppConfig()
    for config in react_app.react_app_configs.merged:
        result = _merge(result, config)

    for module in react_app.modules:
        for config in module.react_app_configs.merged:
            result = _merge(result, config)

    for tool in react_app.service.tools:
        if tool is react_app:
            continue
        for config in tool.react_app_configs.merged:
            result = _merge(result, config)

    return result


def get_flags(app_module):
    return get_config(app_module).flags


class Sections:
    def __init__(self, res):
        self.res = res
        self.config = get_config(res)

    def app_config_imports(self):
        return self.config.index_imports

    def app_config_body(self):
        return self.config.index_body
