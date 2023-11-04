import typing as T
from dataclasses import dataclass

import ramda as R
from moonleap import get_session


@dataclass
class Data:
    django_module: T.Any
    item: T.Any


def get_map_from_item_to_django_module(type_reg, modules):
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

        if django_module:
            lut[type_name] = Data(django_module=django_module, item=item)
        else:
            get_session().warn(f"Module not found: {module_name}")

    return lut
