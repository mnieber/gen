import typing as T

from moonleap import u0

from .add_field_spec import add_field_spec
from .apply_special_rules import apply_special_rules
from .apply_type_updates import apply_type_updates
from .field_spec_from_dict import field_spec_from_dict, is_pass
from .foreign_key import ForeignKey
from .update_or_create_type_spec import update_or_create_type_spec


class TypeSpecParser:
    def __init__(self, type_reg):
        self.type_reg = type_reg

    def parse(self, host, type_spec_dict, type_spec=None):
        # For debugging purposes, we create a new dict that shows how the parser
        # interprets and modifies the type_spec_dict.
        trace = dict()

        items = [
            (key.strip(), value)
            for key, value in type_spec_dict.items()
            if not _is_private_member(key)
        ]
        scalar_items = [item for item in items if not _is_fk_item(item)]
        fk_items = [item for item in items if _is_fk_item(item)]

        if scalar_items and not type_spec:
            raise Exception("The root type spec dict cannot contain scalar fields")

        for key, value in scalar_items:
            # Get field spec and related data from key/value pair
            field_spec_data = field_spec_from_dict(host, key, value)
            trace[field_spec_data["new_key"]] = field_spec_data["new_value"]

            # Add field spec to type spec
            if type_spec:
                if not add_field_spec(type_spec, field_spec_data["field_spec"]):
                    continue

        while fk_items:
            key, value = fk_items.pop(0)

            # Get field spec and related data from key/value pair
            field_spec_data = field_spec_from_dict(host, key, value)
            org_value, value = value, T.cast(T.Dict, field_spec_data["new_value"])
            is_pass = field_spec_data["is_pass"]
            fk = T.cast(ForeignKey, field_spec_data["fk"])
            field_spec = field_spec_data["field_spec"]

            # Add field spec to type spec
            if type_spec:
                if not add_field_spec(type_spec, field_spec):
                    continue

            # Get/update the target type
            if field_spec.field_type in ("fk", "relatedSet", "form"):
                fk_type_spec = update_or_create_type_spec(
                    host,
                    self.type_reg,
                    fk.data.var_type,
                    (u0(value["__base_type__"]) if "__base_type__" in value else None),
                    fk.data.parts,
                    fk.data.module_name or value.get("__module__"),
                    parent_type_spec=type_spec,
                )
                apply_special_rules(fk_type_spec, value, fk, parent_type_spec=type_spec)

                #
                # Use recursion to convert child type specs
                #
                fk_trace = self.parse(host, value, fk_type_spec)

                # Set related name.
                if field_spec.field_type == "fk" and fk.data.related_name:
                    field_spec.related_name = fk.data.related_name

                # Update trace
                if fk.data.parts:
                    fk_trace["__attrs__"] = ".".join(fk.data.parts)
                trace[fk.data.key] = org_value if is_pass else fk_trace

        if "__update__" in type_spec_dict:
            trace["__update__"] = type_spec_dict["__update__"]
            apply_type_updates(host, type_spec, type_spec_dict["__update__"])

        return trace


def _is_private_member(key):
    return key.startswith("__")


def _is_fk_item(item):
    return (
        isinstance(item[1], dict)
        or is_pass(item[1])
        or item[0].endswith("Id")
        or item[0].endswith("Ids")
    )
