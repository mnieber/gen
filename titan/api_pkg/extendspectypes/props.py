from moonleap.resources.type_spec_store import FieldSpec, type_spec_store


def fk_type_spec(self: FieldSpec):
    target = self.field_type_attrs.get("target")
    if not target:
        return None

    return type_spec_store().get(target)
