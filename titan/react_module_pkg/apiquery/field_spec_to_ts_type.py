from moonleap import upper0


def field_spec_to_ts_type(field_spec):
    if field_spec.field_type in ("string", "json", "url", "slug", "uuid"):
        return "string"

    if field_spec.field_type in ("boolean",):
        return "boolean"

    if field_spec.field_type in ("fk", "related_set"):
        return f"{upper0(field_spec.field_type_attrs['target'])}T"

    if field_spec.field_type in ("form",):
        return f"{upper0(field_spec.field_type_attrs['target'])}FormT"

    raise Exception(f"Cannot deduce typescript type for {field_spec.field_type}")
