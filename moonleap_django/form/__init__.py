import moonleap.resource.props as P
from moonleap import extend, kebab_to_camel, tags
from moonleap.verbs import processes
from moonleap_django.module import Module

from .resources import Form


@tags(["form"])
def create_form(term, block):
    form = Form(item_name=kebab_to_camel(term.data) + "Form")
    return form


@extend(Module)
class ExtendModule:
    forms = P.children(processes, "form")
