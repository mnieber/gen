import os

from leapreact.component.props import concat_paths


def policy_lines(store_provider):
    result = []
    return os.linesep.join(result)


def submodules(store_provider):
    return store_provider.app_module.submodules.merged
