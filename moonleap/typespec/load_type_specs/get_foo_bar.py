import typing as T
from dataclasses import dataclass


@dataclass
class Data:
    var: T.Optional[str] = None
    var_type: T.Optional[str] = None
    field_type: T.Optional[str] = None


def get_foo_bar(key):

    #
    # through
    #
    parts_through = key.split(" through ")
    if len(parts_through) == 2:
        foo, bar = Data(), Data()
        _process_data(foo, parts_through[0])
        _process_data(bar, parts_through[1])
    else:
        foo, bar = Data(), None
        _process_data(foo, key)

    return foo, bar


def _process_data(data, value):
    parts_as = value.split(" as ")
    if len(parts_as) == 2:
        data.var, data.var_type = parts_as
    else:
        data.var, data.var_type = None, value
