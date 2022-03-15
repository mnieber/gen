def _on_delete(field):
    return (
        "models.CASCADE"
        if field.field_type_attrs.get("onDelete", "") == "cascade"
        else "models.SET_NULL"
    )
