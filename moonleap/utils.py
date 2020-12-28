import os


def chop0(x):
    return x[1:] if x.startswith(os.linesep) else x


def str_to_type_id(x):
    return ".".join(x.split(".")[-2:])
