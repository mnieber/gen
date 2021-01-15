from .resources import OutputPath


def merge(acc, x):
    return OutputPath(location=(x.location + acc.location))
