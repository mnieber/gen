from moonleap import u0


def field_spec_to_ts_type(field_spec, fk_as_str):
    if field_spec.field_type in ("string", "json", "url", "slug", "uuid"):
        return "string"

    if field_spec.field_type in ("boolean",):
        return "boolean"

    if field_spec.field_type in ("fk",):
        return (
            "string" if fk_as_str else f"{u0(field_spec.field_type_attrs['target'])}T"
        )

    if field_spec.field_type in ("related_set",):
        return (
            "[string]"
            if fk_as_str
            else f"[{u0(field_spec.field_type_attrs['target'])}T]"
        )

    if field_spec.field_type in ("form",):
        return f"{u0(field_spec.field_type_attrs['target'])}FormT"

    raise Exception(f"Cannot deduce typescript type for {field_spec.field_type}")
