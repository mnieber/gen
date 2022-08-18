from moonleap.utils.inflect import plural


def named_item_list_output_field_name(named_item_list):
    return (
        named_item_list.name
        if named_item_list.name
        else plural(named_item_list.typ.item.item_name)
    )
