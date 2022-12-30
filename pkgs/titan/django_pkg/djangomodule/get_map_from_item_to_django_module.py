import typing as T
from dataclasses import dataclass

import ramda as R


@dataclass
class Data:
    django_module: T.Any
    parents: T.Any
    item: T.Any


def get_map_from_item_to_django_module(type_reg, modules):
    items = []
    lut = {}

    for item in type_reg.items:
        type_name = item.type_spec.type_name

        module_name = item.type_spec.module_name
        django_module = item.item_list.django_module

        if django_module and module_name:
            if django_module.name != module_name:
                raise Exception(
                    f"Item {type_name} is in module {module_name} but has django_module {django_module.name}"
                )
        if module_name and not django_module:
            django_module = R.head([x for x in modules if x.name == module_name])
            if not django_module:
                raise Exception(f"Module not found: {module_name}")

        if django_module:
            lut[type_name] = Data(django_module=django_module, parents=[], item=item)
        else:
            items.append(item)
            maybe_parents = type_reg.parents_by_type_name[type_name]
            lut[type_name] = Data(django_module=None, parents=maybe_parents, item=item)

    changed = True
    while changed and len(items):
        changed = False

        for i in reversed(range(len(items))):
            item = items[i]
            type_name = item.type_spec.type_name
            data = lut[type_name]

            for parent in list(data.parents):
                django_module = lut[parent].django_module
                if django_module:
                    if data.django_module and data.django_module != django_module:
                        raise Exception(
                            f"Item {type_name} has two django modules: "
                            + f"{data.django_module} and {django_module}"
                        )
                    data.django_module = django_module
                    data.parents.remove(parent)
                    changed = True

                    if not data.parents:
                        items.pop(i)

    if len(items):
        raise Exception(f"Could not find django module for {items}")

    return lut
