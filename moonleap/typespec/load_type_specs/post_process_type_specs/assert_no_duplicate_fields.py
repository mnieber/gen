from moonleap.utils.fp import count


def assert_no_duplicate_fields(type_spec):
    for derived in (True, False):
        field_names = [
            field_spec.name
            for field_spec in type_spec.field_specs
            if bool(field_spec.derived) == derived
        ]
        for field_name in field_names:
            if count(lambda x: x == field_name, field_names) > 1:
                infix = "derived " if derived else ""
                raise Exception(
                    f"Duplicate {infix}field name {field_name} in type {type_spec.type_name}"
                )
