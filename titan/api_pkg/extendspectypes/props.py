from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.type_spec_store import type_spec_store


def field_spec_target_type_spec(self: FieldSpec):
    if not self.target:
        return None

    return type_spec_store().get(
        self.target + ("Form" if self.field_type == "form" else "")
    )
