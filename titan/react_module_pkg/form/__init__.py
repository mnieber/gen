from moonleap import kebab_to_camel, tags

from .resources import Form


@tags(["form"])
def create_form(term, block):
    form = Form(name=kebab_to_camel(term.data) + "Form")
    return form
