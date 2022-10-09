import typing as T
from dataclasses import dataclass

from moonleap.typespec.load_type_specs.get_generic_field_attrs import (
    get_generic_field_attrs,
)
from moonleap.utils.case import u0


@dataclass
class Data:
    var: T.Optional[str] = None
    var_type: T.Optional[str] = None
    is_parent: T.Optional[bool] = None
    field_type: T.Optional[str] = None


def get_fk_field_attrs(key, init, init_target):
    init_parts = init.split(".") if init else []
    init_target_parts = init_target.split(".") if init_target else []

    foo_parts = init_target_parts or init_parts
    bar_parts = init_parts

    field_attrs = get_generic_field_attrs(key, foo_parts)
    type_attrs = {"field_specs": []}

    foo, bar = Data(), Data()

    #
    # through
    #
    parts_through = key.split(" through ")
    if len(parts_through) == 2:
        foo.var_type, bar.var_type = parts_through
    else:
        foo.var_type = key

    #
    # foo as bar
    #
    if foo.var_type:
        _process_data(foo)

    if bar.var_type:
        _process_data(bar)

    # set results
    field_attrs["target"] = foo.var_type
    field_attrs["field_type"] = foo.field_type
    type_attrs["type_name"] = foo.var_type
    field_attrs["name"] = foo.var

    if "is_sorted" in foo_parts:
        type_attrs["is_sorted"] = True

    if "is_entity" in foo_parts:
        type_attrs["is_entity"] = True

    if "admin_inline" in foo_parts:
        field_attrs["admin_inline"] = True

    if "set_null" in foo_parts:
        field_attrs["set_null"] = True

    if "extract_gql_fields" in foo_parts:
        type_attrs["extract_gql_fields"] = True

    field_attrs["is_parent_of_target"] = foo.is_parent

    if bar.var:
        field_attrs["through_as"] = bar.var

    if bar.var_type:
        type_attrs["type_name"] = field_attrs["through"] = bar.var_type
        field_attrs["is_parent_of_through"] = bar.is_parent

    return key, type_attrs, field_attrs


def _process_data(data):
    parts_as = data.var_type.split(" as ")
    if len(parts_as) == 2:
        data.var, data.var_type = parts_as

    if data.var_type != "+":
        if not data.var:
            # By default, name the field after its type
            data.var = data.var_type

        data.var_type = u0(data.var_type)
        if data.var_type.endswith("Set"):
            data.var_type = data.var_type[:-3]
            data.field_type = "relatedSet"
        else:
            data.field_type = "fk"
