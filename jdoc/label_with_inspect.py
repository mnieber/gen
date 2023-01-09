import inspect


def label():
    def extract(name):
        return type(arg_info.locals[name]).__name__

    f = inspect.currentframe()
    assert f
    arg_info = inspect.getargvalues(f.f_back)
    parts = [extract(name) for name in arg_info.args[1:]]
    return " ".join(parts)
