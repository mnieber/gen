import typing as T

import ramda as R
from moonleap import is_private_key, l0, u0

from .add_extra_model_fields import add_extra_model_fields
from .add_field_spec import add_field_spec
from .field_spec_from_dict import field_spec_from_dict, is_pass
from .foreign_key import ForeignKey
from .update_or_create_type_spec import update_or_create_type_spec


class TypeSpecParser:
    def __init__(self, type_reg):
        self.type_reg = type_reg

    def parse(self, host, type_spec_dict, parent_type_spec=None):
        # For debugging purposes, we create a new dict that shows how the parser
        # interprets and modifies the type_spec_dict.
        trace = dict()

        # Stores the keys that we add to parent_type_spec in this iteration.
        keys = []

        items = [
            (key.strip(), value)
            for key, value in type_spec_dict.items()
            if not is_private_key(key)
        ]

        scalar_items = [item for item in items if not _is_fk_item(item)]
        fk_items = [item for item in items if _is_fk_item(item)]

        if scalar_items and not parent_type_spec:
            raise Exception("The root type spec dict cannot contain scalar fields")

        for key, value in scalar_items:
            # Get field spec and related data from key/value pair
            field_spec_data = field_spec_from_dict(host, key, value)
            field_spec = field_spec_data["field_spec"]
            trace[field_spec_data["new_key"]] = field_spec_data["new_value"]

            # Add field spec to type spec
            if parent_type_spec:
                add_field_spec(parent_type_spec, field_spec)
                keys.append(field_spec.key)

        while fk_items:
            key, value = fk_items.pop(0)

            # Get field spec and related data from key/value pair
            field_spec_data = field_spec_from_dict(host, key, value)
            org_value, value = value, T.cast(T.Dict, field_spec_data["new_value"])
            is_pass = field_spec_data["is_pass"]
            fk = T.cast(ForeignKey, field_spec_data["fk"])
            field_spec = field_spec_data["field_spec"]

            # Add field spec to type spec
            if parent_type_spec:
                add_field_spec(parent_type_spec, field_spec)
                keys.append(field_spec.key)

            # Get/update the target type
            if field_spec.field_type in ("fk", "relatedSet", "form"):
                fk_type_spec = update_or_create_type_spec(
                    host,
                    self.type_reg,
                    fk.var_type,
                    (u0(value["__base_type__"]) if "__base_type__" in value else None),
                    fk.parts,
                    fk.module_name or value.get("__module__"),
                    parent_type_spec=parent_type_spec,
                )
                if "omit_model" not in fk.parts:
                    add_extra_model_fields(
                        fk_type_spec, value, fk, parent_type_spec=parent_type_spec
                    )

                #
                # Use recursion to convert child type specs
                #
                fk_trace, fk_keys = self.parse(host, value, parent_type_spec=fk_type_spec)

                # Set related name.
                if parent_type_spec and field_spec.field_type in ("fk", "relatedSet"):
                    _set_related_name(field_spec=field_spec, type_spec=fk_type_spec, keys=fk_keys)

                # Update trace
                if fk.parts:
                    fk_trace["__attrs__"] = ",".join(fk.parts)
                trace[_trace_key(fk)] = org_value if is_pass else fk_trace

        return trace, keys


def _is_fk_item(item):
    return isinstance(item[1], dict) or is_pass(item[1])


def _trace_key(fk):
    suffix = (
        "Set"
        if fk.field_type == "relatedSet"
        else "Form"
        if fk.field_type == "form"
        else "Id"
        if fk.field_type == "id"
        else "Ids"
        if fk.field_type == "uuid[]"
        else ""
    )
    return (
        f"{fk.maybe_var} as {l0(fk.var_type)}{suffix}"
        if fk.maybe_var
        else fk.default_var
    )


def _set_related_name(field_spec, type_spec, keys):
    related_field_spec = None
    for key in keys:
        rhs_field_spec = type_spec.get_field_spec_by_key(key)
        if rhs_field_spec.is_inverse:
            if related_field_spec:
                raise Exception(
                    f"Multiple inverse fields in {type_spec.type_name} for {field_spec.key}"
                )
            related_field_spec = rhs_field_spec

    if not related_field_spec:
        return

    if field_spec.field_type == "relatedSet":
        if related_field_spec.field_type != "fk":
            raise Exception(
                f"Field {field_spec.key} in {type_spec.type_name} is not a fk"
            )
        related_field_spec.related_name = field_spec.name
    else:
        if related_field_spec.field_type != "relatedSet":
            raise Exception(
                f"Field {field_spec.key} in {type_spec.type_name} is not a relatedSet"
            )
        field_spec.related_name = related_field_spec.name
