from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def item_list_type_spec(item_list):
    return ml_type_spec_from_item_name(item_list.item_name)


def named_item_list_output_field_name(named_item_list):
    return (
        named_item_list.name if named_item_list.name else named_item_list.typ.item_name
    )
