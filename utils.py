import os


def chop0(x):
    return x[1:] if x.startswith(os.linesep) else x
