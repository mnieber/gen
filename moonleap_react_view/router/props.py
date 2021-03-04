from moonleap.utils.case import title0
from moonleap.utils.inflect import plural


def get_modules(self):
    modules = [self.module] + list(self.module.submodules.merged)
    return [x for x in modules if x.store]


def get_item_types(self):
    result = []
    for module in get_modules(self):
        result.extend(module.store.item_types)
    return result


def has_list_view(self, name):
    for module in get_modules(self):
        for list_view in module.list_views:
            if list_view.item_name == name:
                return True
    return False


def has_form_view(self, name):
    for module in get_modules(self):
        for form_view in module.form_views:
            if form_view.item_name == name:
                return True
    return False


def get_imports(self, name):
    result = []
    has_list_view = self.has_list_view(name)
    has_form_view = self.has_form_view(name)

    if has_list_view or has_form_view:
        result.append(f"Load{title0(plural(name))}Effect")

    if has_list_view:
        result.append(f"{title0(name)}ListView")

    if has_form_view:
        result.append(f"{title0(name)}FormView")

    return ", ".join(result)
