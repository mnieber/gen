def prop_or(default_value, prop_name):
    def f(x):
        if hasattr(x, prop_name):
            return getattr(x, prop_name)

        if isinstance(x, dict) and prop_name in x:
            return x[prop_name]

        return default_value

    return f


def ds(f):
    return lambda x: f(*x)


def uniq(items):
    result = []
    for x in items:
        if x not in result:
            result.append(x)
    return result
