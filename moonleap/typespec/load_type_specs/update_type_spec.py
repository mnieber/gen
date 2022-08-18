import typing as T

from moonleap.typespec.field_spec import FkFieldSpec
from moonleap.typespec.load_type_specs.get_field_spec import get_field_spec
from moonleap.typespec.load_type_specs.set_is_reverse_of_fk_value import (
    set_is_reverse_of_fk_value,
)
from moonleap.typespec.type_spec import TypeSpec


def update_type_spec(
    type_spec_store, type_attrs, type_spec_dict, parent_node, first_pass
):
    type_spec = type_spec_store.get(type_attrs["type_name"], None)
    if type_attrs["type_name"] == "+":
        if type_spec_dict.items():
            raise Exception('Cannot add fields to the special "+" through type')
        return

    # Create or update the type spec
    if first_pass:
        if not type_spec:
            type_spec = TypeSpec(**type_attrs)
            type_spec_store.setdefault(type_spec.type_name, type_spec)
        else:
            for type_attr, value in type_attrs.items():
                if value is not None and type_attr not in ("field_specs", "type_name"):
                    setattr(type_spec, type_attr, value)
    else:
        assert type_spec

    # Add the field specs (on the first pass)
    if first_pass:
        type_spec_dict["__type_name__"] = type_spec.type_name
        type_spec_dict["__field_names__"] = []
        for key, field_spec_value in type_spec_dict.items():
            if key.startswith("__"):
                continue

            field_spec = get_field_spec(
                type_spec_store,
                key,
                field_spec_value,
                parent_node=type_spec_dict,
                first_pass=first_pass,
            )
            type_spec.field_specs.append(field_spec)
            type_spec_dict["__field_names__"].append(field_spec.name)

    # If in the second pass, then this is our chance to determine if the fk field spec
    # is the reverse of another relatedSet field spec (we need the parent_node for that,
    # so that we can determine pairs of fk/relatedSet).
    if not first_pass:
        for field_name in type_spec_dict["__field_names__"]:
            field_spec = type_spec.get_field_spec(field_name, False)
            if field_spec and field_spec.field_type == "fk":
                set_is_reverse_of_fk_value(
                    type_spec_store,
                    type_spec,
                    T.cast(FkFieldSpec, field_spec),
                    parent_node,
                )

    return type_spec
