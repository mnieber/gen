from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def item_type_spec(item):
    return ml_type_spec_from_item_name(item.item_name)


def named_item_output_field_name(named_item):
    return named_item.name if named_item.name else named_item.typ.item_name
