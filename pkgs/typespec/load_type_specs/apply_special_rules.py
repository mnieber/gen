from moonleap import l0

from .foreign_key import ForeignKey


def apply_special_rules(type_spec, value, fk: ForeignKey, parent_type_spec=None):
    # Add an auto-field for the entity id
    if (
        type_spec.is_entity
        and not type_spec.get_field_spec_by_key("id")
        and not value.get("id")
    ):
        value["id"] = "Id.primary_key.auto"

    # Add an auto-field for the sortPos
    if (
        type_spec.is_sorted
        and not type_spec.get_field_spec_by_key("sortPos")
        and not value.get("sortPos")
    ):
        value["sortPos|"] = "Int = 0"

    # If we are adding a related set, then create a related fk auto-field that points back
    # to the parent type-spec. Note that this auto-field may be added to the type spec and then
    # removed again if some non-auto field is using the same name.
    if (
        fk.data.field_type == "relatedSet"
        and parent_type_spec
        and "omit_model" not in fk.data.parts
    ):
        key = l0(parent_type_spec.type_name) + f" with {fk.var}"
        if key not in value:
            required = "is_owner" in fk.data.parts
            value[key] = "pass.auto" + ("" if required else ".optional")
