from moonleap import kebab_to_camel, create

from .resources import Form


@create(["form"])
def create_form(term, block):
    form = Form(name=kebab_to_camel(term.data) + "Form")
    return form
