from moonleap.utils.case import u0


def ts_type_from_item_name(x):
    return f"{u0(x)}T"


def ts_form_type_from_item_name(x):
    return f"{u0(x)}FormT"


def item_ts_type(item):
    return ts_type_from_item_name(item.item_name)


def item_type_ts_type_import_path(item_type):
    return f"src/api/types/{item_type.name}"


def item_list_ts_type(item_list):
    return f"[{ts_type_from_item_name(item_list.item_name)}]"


def item_type_ts_type(item_type):
    return ts_type_from_item_name(item_type.name)


def item_type_ts_form_type(item_type):
    return ts_form_type_from_item_name(item_type.name)
