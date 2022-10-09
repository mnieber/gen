from moonleap.typespec.field_spec import get_field_spec_constructor
from moonleap.typespec.load_type_specs.get_fk_field_attrs import get_fk_field_attrs
from moonleap.typespec.load_type_specs.update_type_spec import update_type_spec


def get_fk_field_spec(type_spec_store, key, field_spec_value):
    (key, type_attrs, field_attrs) = get_fk_field_attrs(
        key, field_spec_value.get("__init__"), field_spec_value.get("__init_target__")
    )

    update_type_spec(type_spec_store, type_attrs, field_spec_value)

    return get_field_spec_constructor(field_attrs["field_type"])(**field_attrs)
