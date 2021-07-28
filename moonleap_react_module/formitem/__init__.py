from moonleap import kebab_to_camel, tags

from .resources import FormItem


@tags(["form-item"])
def create_form_item(term, block):
    form_item = FormItem(item_name=kebab_to_camel(term.data))
    return form_item
