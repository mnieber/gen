from titan.react_pkg.pkg.ts_var import (
    ts_form_type_from_item_name,
    ts_type_from_item_name,
)


def field_spec_to_ts_type(field_spec, fk_as_str):
    if field_spec.field_type in ("string", "json", "url", "slug", "uuid"):
        return "string"

    if field_spec.field_type in ("boolean",):
        return "boolean"

    if field_spec.field_type in ("fk",):
        if fk_as_str:
            return "string"
        item_name = field_spec.target
        return ts_type_from_item_name(item_name)

    if field_spec.field_type in ("relatedSet",):
        if fk_as_str:
            return "string[]"
        item_name = field_spec.target
        return f"[{ts_type_from_item_name(item_name)}]"

    if field_spec.field_type in ("form",):
        item_name = field_spec.target
        return ts_form_type_from_item_name(item_name)

    if field_spec.field_type in ("idList",):
        return "string[]"

    raise Exception(f"Cannot deduce typescript type for {field_spec.field_type}")
