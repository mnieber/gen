from moonleap.typespec.load_type_specs.get_foo_bar import get_foo_bar
from moonleap.utils.case import u0

from .get_generic_field_attrs import get_generic_field_attrs


def get_fk_field_attrs(key, init, init_target):
    init_parts = init.split(".") if init else []
    init_target_parts = init_target.split(".") if init_target else []

    field_attrs = get_generic_field_attrs(key, init_parts)
    type_attrs = {"field_specs": []}

    foo, bar = get_foo_bar(key)
    _extract_type(foo)
    if bar:
        _extract_type(bar)

    # set results
    field_attrs["target"] = foo.var_type
    field_attrs["field_type"] = foo.field_type
    type_attrs["type_name"] = foo.var_type
    field_attrs["key"] = foo.var

    if "is_sorted" in init_parts:
        type_attrs["is_sorted"] = True

    if "help" in init_parts:
        field_attrs["help"] = True

    if "entity" in init_parts:
        type_attrs["is_entity"] = True

    if "admin_inline" in init_parts:
        field_attrs["admin_inline"] = True

    if "set_null" in init_parts:
        field_attrs["set_null"] = True

    if "extract_gql_fields" in init_parts:
        type_attrs["extract_gql_fields"] = True

    field_attrs["is_parent_of_target"] = "is_parent" in init_parts

    if bar and bar.var:
        field_attrs["through_as"] = bar.var

    if bar and bar.var_type:
        type_attrs["type_name"] = field_attrs["through"] = bar.var_type
        field_attrs["is_parent_of_through"] = "is_parent" in init_target_parts

    return key, type_attrs, field_attrs


def _extract_type(data):
    if not data.var:
        data.var = data.var_type

    if data.var_type.endswith("Set"):
        data.var_type = data.var_type[:-3]
        data.field_type = "relatedSet"
    else:
        data.field_type = "fk"

    data.var_type = u0(data.var_type)
