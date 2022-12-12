from moonleap import create, kebab_to_camel, named
from titan.types_pkg.typeregistry.resources import ItemList

base_tags = {
    "item~list": ["pipeline-elm"],
}


@create("item~list")
def create_item_list(term):
    from titan.types_pkg.typeregistry import get_type_reg

    item_name = kebab_to_camel(term.data)
    return get_type_reg().get_item_list(item_name)


@create("x+item~list")
def create_named_item(term):
    return named(ItemList)()
