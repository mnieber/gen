import typing as T
from dataclasses import dataclass

from moonleap.typespec.load_type_specs.get_scalar_field_attrs import (
    get_scalar_field_attrs,
)
from moonleap.utils.case import u0
from moonleap.utils.pop import pop


@dataclass
class Data:
    var: T.Optional[str] = None
    var_type: T.Optional[str] = None
    is_entity: T.Optional[bool] = None
    set_null: T.Optional[bool] = None
    is_parent: T.Optional[bool] = None
    is_sorted: T.Optional[bool] = None
    admin_inline: T.Optional[bool] = None
    extract_gql_fields: T.Optional[bool] = None
    field_type: T.Optional[str] = None


def get_fk_field_attrs(key, init, init_target):
    key = key.replace("_", "")
    init_parts = init.split(".") if init else []
    init_target_parts = init_target.split(".") if init_target else []

    # Using the example of foo.var as foo.var_type through bar.var as bar.var_type
    foo = Data()
    bar = Data()

    key, field_attrs = get_scalar_field_attrs(key)
    if "name" in field_attrs:
        del field_attrs["name"]
    type_attrs = {"field_specs": []}

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
        _process_data(foo, init_target_parts if bar.var_type else init_parts)

    if bar.var_type:
        _process_data(bar, init_parts)

    # set results
    field_attrs["target"] = foo.var_type
    field_attrs["field_type"] = foo.field_type
    type_attrs["type_name"] = foo.var_type
    field_attrs["name"] = foo.var

    if foo.is_sorted:
        type_attrs["is_sorted"] = True

    if foo.is_entity:
        type_attrs["is_entity"] = True

    if foo.admin_inline:
        field_attrs["admin_inline"] = True

    if foo.set_null:
        field_attrs["set_null"] = True

    if foo.extract_gql_fields:
        type_attrs["extract_gql_fields"] = True

    field_attrs["is_parent_of_target"] = foo.is_parent

    if bar.var:
        field_attrs["through_as"] = bar.var

    if bar.var_type:
        type_attrs["type_name"] = field_attrs["through"] = bar.var_type
        field_attrs["is_parent_of_through"] = bar.is_parent

    return key, type_attrs, field_attrs


def _process_data(data, init_parts):
    parts_as = data.var_type.split(" as ")
    if len(parts_as) == 2:
        data.var, data.var_type = parts_as

    data.var_type, is_parent = pop(data.var_type, "$")
    if is_parent:
        data.is_parent = True

    data.var_type, is_sorted = pop(data.var_type, ">")
    if is_sorted:
        data.is_sorted = True

    data.var_type, admin_inline = pop(data.var_type, "=")
    if admin_inline or "admin_inline" in init_parts:
        data.admin_inline = True

    data.var_type, is_entity = pop(data.var_type, "@")
    if is_entity:
        data.is_entity = True

    if "extract_gql_fields" in init_parts:
        data.extract_gql_fields = True

    if "set_null" in init_parts:
        data.set_null = True

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
