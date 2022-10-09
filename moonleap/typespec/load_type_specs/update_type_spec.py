from moonleap.typespec.load_type_specs.get_field_spec import get_field_spec
from moonleap.typespec.type_spec import TypeSpec


def update_type_spec(type_spec_store, type_attrs, type_spec_dict):
    type_spec = type_spec_store.get(type_attrs["type_name"], None)
    if type_attrs["type_name"] == "+":
        if [x for x in type_spec_dict.items() if not x[0].startswith("__")]:
            raise Exception('Cannot add fields to the special "+" through type')
        return

    # Create or update the type spec
    if not type_spec:
        type_spec = TypeSpec(**type_attrs)
        type_spec_store.setdefault(type_spec.type_name, type_spec)
    else:
        for type_attr, value in type_attrs.items():
            if value is not None and type_attr not in ("field_specs", "type_name"):
                setattr(type_spec, type_attr, value)

    # Add the field specs
    for key, field_spec_value in type_spec_dict.items():
        if key.startswith("__"):
            continue

        field_spec = get_field_spec(type_spec_store, key, field_spec_value)
        if field_spec.field_type == "fk":
            maybe_set_reverse_of_related_set(field_spec_value, field_spec)

        type_spec.field_specs.append(field_spec)

    return type_spec


def maybe_set_reverse_of_related_set(field_spec_value, field_spec):
    parent_field = field_spec_value.get("__is_reverse_of_related_set__", None)
    if parent_field:
        field_spec.is_reverse_of_related_set = parent_field
