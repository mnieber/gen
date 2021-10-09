from moonleap.utils.case import sn


def field_spec_default_value(field_spec):
    t = field_spec.field_type

    if t == "fk":
        return f"{sn(field_spec.name)}.id"

    if t == "boolean":
        return r"True"

    if t == "date":
        return r'"01-02-2003"'

    if t == "email":
        return r"email@email.com"

    if t == "slug":
        return r'"foo-bar"'

    if t == "uuid":
        return r'"41f55a14-a1b7-5697-84ef-c00e3f51c7e2"'

    if t == "string":
        return r'"foo"'

    if t == "url":
        return r'"https://foo.bar.com"'

    raise Exception(f"Unknown graphene field type: {t} in spec for {field_spec.name}")
