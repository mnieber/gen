from moonleap.parser.term import word_to_term


def get_named_data_term(widget_spec, name):
    value = widget_spec.get_value_by_name(name)
    if value and "+" not in value:
        raise Exception(f"Expected + in value: {value}")
    return word_to_term(value) if value else None


def get_named_item_list_term(widget_spec):
    return get_named_data_term(widget_spec, "items")


def get_named_item_term(widget_spec):
    return get_named_data_term(widget_spec, "item")
