import os

from leapreact.component.props import concat_paths


def policy_lines(store_provider):
    result = []
    return os.linesep.join(result)


def substores(store_provider):
    submodules = store_provider.app_module.submodules.merged
    return [x.store for x in submodules]
