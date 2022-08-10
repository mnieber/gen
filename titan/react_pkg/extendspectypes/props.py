from moonleap.utils.case import l0, u0
from moonleap.utils.inflect import plural


def ts_type_from_item_name(x):
    return f"{u0(x)}T"


def ts_form_type_from_item_name(x):
    return f"{u0(x)}FormT"


def item_ts_type(item):
    return ts_type_from_item_name(item.item_name)


def item_ts_var(item):
    return item.item_name


def item_list_ts_type(item_list):
    return f"[{ts_type_from_item_name(item_list.item_name)}]"


def item_list_ts_var(item_list):
    return plural(item_list.item_name)


def item_type_ts_type(item_type):
    return ts_type_from_item_name(item_type.name)


def item_type_ts_form_type(item_type):
    return ts_form_type_from_item_name(item_type.name)


def field_spec_ts_type(field_spec):
    if field_spec.field_type in ("fk", "uuid") and field_spec.target:
        return f"{field_spec.target}T"

    if field_spec.field_type in ("string", "json", "url", "slug", "uuid"):
        return "string"

    if field_spec.field_type in ("boolean",):
        return "boolean"

    if field_spec.field_type in ("int", "float"):
        return "number"

    if field_spec.field_type in ("form",):
        return f"{field_spec.target}FormT"

    raise Exception(f"Cannot deduce graphql type for {field_spec.field_type}")


def field_spec_ts_default_value(field_spec):
    if field_spec.field_type in ("string", "json", "url", "slug"):
        return "''"

    if field_spec.field_type in ("boolean",):
        return "false"

    if field_spec.field_type in ("int", "float"):
        return "0"

    raise Exception(f"Cannot deduce ts default value for {field_spec.field_type}")
