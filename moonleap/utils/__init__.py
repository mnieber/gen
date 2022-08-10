import os
from io import StringIO

import yaml
from yaml import dump


def chop0(x):
    return x[1:] if x.startswith(os.linesep) else x


def chop(x):
    return x[:-1] if x.endswith(os.linesep) else x


def yaml2dict(x):
    s = StringIO(chop0(x))
    return yaml.safe_load(s)


def dict2yaml(x):
    return dump(x)


def dbg(x):
    import pudb

    pudb.set_trace()
    return x


def maybe_tuple_to_tuple(x):
    return x if isinstance(x, tuple) else (x,)
