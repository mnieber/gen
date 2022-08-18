from moonleap.utils.case import sn


def module_path(self):
    return sn(self.name)


def get_module_by_name(django_app, module_name, default="__notset__"):
    for x in django_app.modules:
        if x.name == module_name:
            return x

    if default == "__notset__":
        raise KeyError(f"No module named {module_name}")

    return default


def item_django_module(item):
    return item.item_list.django_module if item.item_list else None
