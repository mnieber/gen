from moonleap import u0
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import type_spec_store


def target_type_spec(self: FieldSpec):
    target = self.target
    if not target:
        return None

    return type_spec_store().get(
        u0(target) + ("Form" if self.field_type == "form" else "")
    )
