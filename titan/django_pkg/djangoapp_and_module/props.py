def get_module_by_name(django_app, module_name):
    for x in django_app.modules:
        if x.name == module_name:
            return x
    return None
