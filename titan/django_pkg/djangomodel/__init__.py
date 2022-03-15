from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    StoreOutputPaths,
    StoreTemplateDirs,
    create,
    empty_rule,
    extend,
    rule,
)
from moonleap.utils.case import kebab_to_camel
from moonleap.verbs import contains, has, provides

from .resources import DjangoModel, import_type_spec

rules = [(("module", contains + provides, "item~list"), empty_rule())]

base_tags = [("module", ["django-module"])]


@create("django-model")
def create_module(term):
    django_model = DjangoModel(name=kebab_to_camel(term.data))
    return django_model


@rule("django-model", provides, "item~list")
def django_model_provides_item_list(django_model, item_list):
    import_type_spec(item_list.type_spec, django_model)


@extend(DjangoModel)
class ExtendDjangoModel(StoreTemplateDirs, StoreOutputPaths):
    item_list = P.child(provides, "item~list")
    module = P.parent("module", has)
