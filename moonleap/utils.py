import os


def chop0(x):
    return x[1:] if x.startswith(os.linesep) else x


def vendor_id_from_class(x):
    return x.__module__.split(".")[0]


def resource_id_from_class(x):
    return vendor_id_from_class(x) + "." + x.__name__
