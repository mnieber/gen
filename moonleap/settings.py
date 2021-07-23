import os
from pathlib import Path

import ramda as R

from moonleap.utils import yaml2dict
from moonleap.utils.merge_into_config import merge_into_config


def load_settings(settings_fn):
    settings = {}

    global_settings_fn = ".moonleap.config.yml"
    if os.path.exists(global_settings_fn):
        with open(global_settings_fn) as ifs:
            merge_into_config(settings, yaml2dict(ifs.read()))

    fn = Path(settings_fn)
    if not os.path.exists(fn):
        raise Exception(f"Settings file not found: {fn}")
    with open(fn) as ifs:
        merge_into_config(settings, yaml2dict(ifs.read()))

    override_fn = Path(fn).with_suffix(".override.yml")
    if os.path.exists(override_fn):
        with open(override_fn) as ifs:
            merge_into_config(settings, yaml2dict(ifs.read()))

    settings["references"] = R.pipe(
        R.always(settings.setdefault("references", {})),
        R.to_pairs,
        R.map(lambda x: (x[0], x[1][:-1] if x[1].endswith("/") else x[1])),
        R.from_pairs,
    )(None)

    return settings
