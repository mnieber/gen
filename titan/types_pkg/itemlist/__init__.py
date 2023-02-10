from moonleap import create, kebab_to_camel
from titan.types_pkg.typeregistry.resources import ItemList  # noqa: F401


@create("item~list")
def create_item_list(term):
    from titan.types_pkg.typeregistry import get_type_reg

    item_name = kebab_to_camel(term.data)
    return get_type_reg().get_item_list(item_name)
