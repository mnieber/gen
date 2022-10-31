from moonleap.utils.case import l0

from .foreign_key import ForeignKey


def apply_special_rules(type_spec, value, fk: ForeignKey, parent_type_spec=None):
    is_speccing_a_through_type = fk.bar and fk.bar.var_type and fk.bar.var_type != "+"

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

    # If we are adding a related set, then create a related fk auto-field. Note that
    # this auto-field may be added to the type spec and then removed again if some
    # non-auto field matches it.
    if fk.foo.field_type == "relatedSet":
        if parent_type_spec:
            key = l0(parent_type_spec.type_name)
            if not is_speccing_a_through_type:
                key += f" for {fk.var}"
            if key not in value:
                required = is_speccing_a_through_type or "is_owner" in fk.data_parts
                value[key] = "pass.auto" + ("" if required else ".optional")

        # If we speccing a through type, then we also need a related fk to foo.var_type
        if is_speccing_a_through_type:
            assert fk.foo.var_type
            key = l0(fk.foo.var_type)
            if key not in value:
                value[key] = "pass.auto"
            if key not in value:
                value[key] = "pass.auto"
