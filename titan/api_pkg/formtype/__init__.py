from moonleap import create, kebab_to_camel, kebab_to_snake, rule

from . import props
from .resources import FormType


@create(["form-type"])
def create_form_type(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    form_type = FormType(
        name=name,
        name_snake=name_snake,
    )
    return form_type


@rule("item-type")
def item_type_created(item_type):
    props.get_or_create_form_type_spec(item_type.name)
