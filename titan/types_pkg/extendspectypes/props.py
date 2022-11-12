from titan.types_pkg.pkg.field_spec import FkFieldSpec
from titan.types_pkg.typeregistry import get_type_reg


def fk_field_spec_target_type_spec(self: FkFieldSpec):
    if not self.target:
        return None

    return get_type_reg().get(self.target)


def form_field_spec_target_type_spec(self: FkFieldSpec):
    return fk_field_spec_target_type_spec(self)
