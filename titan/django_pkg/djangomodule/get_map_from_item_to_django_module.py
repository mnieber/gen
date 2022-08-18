import typing as T
from dataclasses import dataclass

from moonleap.typespec.type_spec_store import type_spec_store
from titan.api_pkg.typeregistry import get_type_reg


@dataclass
class Data:
    django_module: T.Any
    parents: T.Any
    item: T.Any


def get_map_from_item_to_django_module():
    items = []
    lut = {}

    for item_list in get_type_reg().item_lists:
        item = item_list.item
        type_name = item.type_spec.type_name

        if item.item_list.django_module:
            lut[type_name] = Data(
                django_module=item.item_list.django_module, parents=[], item=item
            )
        else:
            items.append(item)
            parents = type_spec_store().parents_by_type_name[item.type_spec.type_name]
            sure_parents = [x[0] for x in parents if x[1]]
            maybe_parents = [x[0] for x in parents if not x[1]]
            if len(sure_parents) > 1:
                raise Exception(f"More than one sure parent for {type_name}")

            lut[type_name] = Data(
                django_module=None, parents=sure_parents or maybe_parents, item=item
            )

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
