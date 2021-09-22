from moonleap import create, kebab_to_camel, kebab_to_snake, rule
from moonleap.resources.type_spec import form_type_spec_from_data_type_spec

from . import props
from .resources import FormItemType


@create(["form-item-type"])
def create_form_item_type(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    form_item_type = FormItemType(
        name=name,
        name_snake=name_snake,
    )
    return form_item_type


@rule("item-type")
def item_type_created(item_type):
    props.get_or_create_form_type_spec(item_type.name)
