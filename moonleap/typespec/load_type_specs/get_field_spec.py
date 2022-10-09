def get_field_spec(type_spec_store, key, field_spec_value):
    from moonleap.typespec.load_type_specs.get_fk_field_spec import get_fk_field_spec
    from moonleap.typespec.load_type_specs.get_scalar_field_spec import (
        get_scalar_field_spec,
    )

    if isinstance(field_spec_value, dict):
        return get_fk_field_spec(type_spec_store, key, field_spec_value)

    return get_scalar_field_spec(key, field_spec_value)
