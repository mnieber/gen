from moonleap.utils.fp import count


def assert_no_duplicate_fields(type_spec):
    field_keys = [field_spec.key for field_spec in type_spec.field_specs]
    for field_key in field_keys:
        if count(lambda x: x == field_key, field_keys) > 1:
            raise Exception(
                f"Duplicate field {field_key} in type {type_spec.type_name}"
            )
