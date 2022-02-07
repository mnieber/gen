from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def item_type_type_spec(item_type):
    return ml_type_spec_from_item_name(item_type.name)
