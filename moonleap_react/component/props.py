import os

import ramda as R


def concat_paths(path_stores):
    def clean(x):
        x = x.strip()
        if not x.endswith(";"):
            x += ";"
        return x

    result = R.pipe(
        R.always(path_stores),
        R.map(R.prop("paths")),
        R.chain(R.identity),
        R.map(clean),
    )(None)

    return os.linesep.join(result)
