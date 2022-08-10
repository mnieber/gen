_add_function_by_resource_type = {}


def add(resource, child_resource):
    f = _add_function_by_resource_type.get(child_resource.__class__)
    if not f:
        raise Exception(f"No add rule is registered for {child_resource.__class__}")
    f(resource, child_resource)


def register_add(resource_type):
    def wrapped(f):
        _add_function_by_resource_type[resource_type] = f
        return f

    return wrapped
