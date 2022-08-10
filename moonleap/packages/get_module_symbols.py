def get_module_symbols(module):
    return [
        f
        for f in module.__dict__.values()
        if getattr(f, "__module__", "") == module.__name__
    ]
