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


def vendor_id_from_class(x):
    return x.__module__.split(".")[0]


def resource_id_from_class(x):
    return vendor_id_from_class(x) + "." + x.__name__


def dbg(x):
    __import__("pudb").set_trace()
    return x


def maybe_tuple_to_tuple(x):
    return x if isinstance(x, tuple) else (x,)
