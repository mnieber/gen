from titan.types_pkg.pkg.field_spec import FieldSpec, FkFieldSpec
from titan.types_pkg.typeregistry import get_type_reg


def fk_field_spec_target_type_spec(self: FkFieldSpec):
    if not self.target:
        return None

    return get_type_reg().get(self.target)


def form_field_spec_target_type_spec(self: FkFieldSpec):
    return fk_field_spec_target_type_spec(self)


def field_spec_graphql_type(self: FieldSpec, host):
    postfix = "" if self.is_optional(host) else "!"

    if self.field_type in (
        "string",
        "text",
        "json",
        "url",
        "slug",
        "image",
        "markdown",
    ):
        return "String" + postfix

    if self.field_type in ("boolean",):
        return "Boolean" + postfix

    if self.field_type in ("int",):
        return "Int" + postfix

    if self.field_type in ("string[]",):
        return "[String]" + postfix

    if self.field_type in ("int[]",):
        return "[Int]" + postfix

    if self.field_type in ("float",):
        return "Float" + postfix

    if self.field_type in ("uuid",):
        return "ID" + postfix

    if self.field_type in ("uuid[]",):
        return "[String]" + postfix

    if self.field_type in ("form",):
        return f"{self.target_type_spec.type_name}T" + postfix

    raise Exception(f"Cannot deduce graphql type for {self.field_type}")
