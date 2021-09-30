from moonleap import u0
from titan.api_pkg.item.resources import Item


def ml_type_name(x):
    if isinstance(x, Item):
        return ml_type_name_from_item_name(x.item_name)
    raise Exception(f"ml_type_name: unknown {x}")


def ml_type_name_from_item_name(x):
    return u0(x)


def ml_form_type_name_from_type_name(x):
    return x + "Form"


def ml_form_type_name(x):
    return ml_form_type_name_from_type_name(ml_type_name(x))


def ml_form_type_spec_from_item_name(item_name):
    from moonleap.resources.type_spec_store import type_spec_store

    data_type_name = ml_type_name_from_item_name(item_name)
    form_type_name = ml_form_type_name_from_type_name(data_type_name)
    return type_spec_store().get(form_type_name, None)


def ml_type_spec_from_item_name(item_name):
    from moonleap.resources.type_spec_store import type_spec_store

    data_type_name = ml_type_name_from_item_name(item_name)
    return type_spec_store().get(data_type_name, None)
