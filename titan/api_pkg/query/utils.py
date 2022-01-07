from moonleap.utils.case import camel_join
from moonleap.utils.inflect import plural


def get_output_field_name_for_named_item_list(named_item_list_provided):
    item_name = named_item_list_provided.typ.item_name
    output_field_name = camel_join(named_item_list_provided.name, plural(item_name))
    return item_name, output_field_name


def get_output_field_name_for_named_item(named_item_provided):
    item_name = named_item_provided.typ.item_name
    output_field_name = camel_join(named_item_provided.name, item_name)
    return item_name, output_field_name
