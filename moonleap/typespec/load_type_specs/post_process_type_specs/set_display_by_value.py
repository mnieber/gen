import ramda as R


def set_display_by_value(type_spec):
    type_spec.display_item_by = R.head(
        [x.name for x in type_spec.get_field_specs() if x.display]
    )
