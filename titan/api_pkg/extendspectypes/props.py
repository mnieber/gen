from moonleap import u0
from moonleap.resources.field_spec import FieldSpec
from moonleap.resources.type_spec_store import type_spec_store


def fk_type_spec(self: FieldSpec):
    target = self.field_type_attrs.get("target")
    if not target:
        return None

    return type_spec_store().get(
        u0(target) + ("Form" if self.field_type == "form" else "")
    )
