import typing as T

from moonleap.typespec.load_type_specs.foreign_key import ForeignKey

from .add_field_spec import add_field_spec
from .apply_special_rules import apply_special_rules
from .apply_type_updates import apply_type_updates
from .field_spec_from_dict import field_spec_from_dict, is_pass, is_related_fk
from .update_or_create_type_spec import update_or_create_type_spec


class TypeSpecParser:
    def __init__(self, type_spec_store):
        self.type_spec_store = type_spec_store

    def parse(
        self, host, type_spec_dict, type_spec=None, related_parent_field_name=None
    ):
        # For debugging purposes, we create a new dict that shows how the parser
        # interprets and modifies the type_spec_dict.
        trace = dict()

        items = [x for x in type_spec_dict.items() if not _is_private_member(x[0])]
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
                add_field_spec(type_spec, field_spec_data["field_spec"])

        while fk_items:
            key, value = fk_items.pop(0)

            # Get field spec and related data from key/value pair
            field_spec_data = field_spec_from_dict(
                host, key, value, related_parent_field_name if type_spec else None
            )
            org_value, value = value, field_spec_data["new_value"]
            is_related_fk = field_spec_data["is_related_fk"]
            is_pass = field_spec_data["is_pass"]
            fk = T.cast(ForeignKey, field_spec_data["fk"])

            # Add field spec to type spec
            if type_spec:
                add_field_spec(type_spec, field_spec_data["field_spec"])

            # Get/update type spec
            if fk.data.var_type != "+":
                fk_type_spec = update_or_create_type_spec(
                    self.type_spec_store,
                    fk.data.var_type,
                    fk.data_parts,
                    fk.data.module_name or value.get("__module__"),
                    parent_type_spec=None if is_related_fk else type_spec,
                )
                apply_special_rules(fk_type_spec, value, fk, parent_type_spec=type_spec)

                if fk.bar:
                    assert fk.bar.var_type != "+"

                    # The through type was already created. Now create the target type.
                    update_or_create_type_spec(
                        self.type_spec_store,
                        fk.foo.var_type,
                        fk.target_parts,
                        fk.foo.module_name,
                        parent_type_spec=type_spec,
                    )

                    # We already have a related set to the target type (through the through-type).
                    # Now also add a related set to the through type.
                    fk_items.append(
                        (f"{fk.through_var} as {fk.through_var_type}", "pass")
                    )

                #
                # Use recursion to convert child type specs
                #
                fk_trace = self.parse(
                    host,
                    value,
                    fk_type_spec,
                    related_parent_field_name=None if fk.bar else fk.var,
                )

                # Update trace
                if fk.data_parts:
                    fk_trace["__init__"] = ".".join(fk.data_parts)
                if fk.target_parts:
                    fk_trace["__init_target__"] = ".".join(fk.target_parts)
                trace[fk.clean_key] = (
                    org_value if is_related_fk or is_pass else fk_trace
                )

        if "__update__" in type_spec_dict:
            trace["__update__"] = type_spec_dict["__update__"]
            apply_type_updates(host, type_spec, type_spec_dict["__update__"])

        return trace


def _is_private_member(key):
    return key.startswith("__")


def _is_fk_item(item):
    return isinstance(item[1], dict) or is_related_fk(item[1]) or is_pass(item[1])
