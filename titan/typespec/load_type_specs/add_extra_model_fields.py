def add_extra_model_fields(type_spec, value):
    if (
        type_spec.is_entity
        and not type_spec.get_field_spec_by_key("id")
        and not value.get("id")
    ):
        value["id"] = "Id,primary_key"

    if (
        type_spec.is_sorted
        and not type_spec.get_field_spec_by_key("sortPos")
        and not value.get("sortPos")
    ):
        value["sortPos|"] = "Int = 0"
