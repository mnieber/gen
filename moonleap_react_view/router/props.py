from moonleap.utils.case import title0, untitle0
from moonleap.utils.inflect import plural


def get_item_types(self):
    result = list(self.module.store.item_types)
    for substore in self.module.store.substores:
        result.extend(substore.item_types)
    return result


def has_list_view(self, name):
    return bool([x for x in self.module.list_views.merged if x.item_name == name])


def has_form_view(self, name):
    return bool([x for x in self.module.form_views.merged if x.item_name == name])


def get_imports(self, name):
    result = []
    has_list_view = self.has_list_view(name)
    has_form_view = self.has_form_view(name)

    if has_list_view or has_form_view:
        result.append(f"Load{title0(plural(name))}Effect")

    if has_list_view:
        result.append(f"{title0(plural(name))}ListView")

    if has_form_view:
        result.append(f"{title0(plural(name))}FormView")

    return ", ".join(result)
