from titan.react_pkg.pkg.ts_var import ts_type_from_item_name


def item_ts_type(item):
    return ts_type_from_item_name(item.item_name)


def item_list_ts_type(item_list):
    return f"[{ts_type_from_item_name(item_list.item_name)}]"


def item_type_ts_type(item_type):
    return ts_type_from_item_name(item_type.name)
