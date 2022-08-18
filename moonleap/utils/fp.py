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


def aperture(size, items):
    result = []
    for i in range(0, len(items) - size + 1):
        result.append(items[i : i + size])
    return result


def add_to_list_as_set(l, new_element):
    if new_element not in l:
        l.append(new_element)


def count(condition, items):
    result = 0
    for item in items:
        if condition(item):
            result += 1
    return result
