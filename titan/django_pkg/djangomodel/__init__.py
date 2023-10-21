import moonleap.packages.extensions.props as P
from moonleap import Prop, create, empty_rule, extend, rule
from moonleap.blocks.verbs import contains, has, provides
from moonleap.utils.case import kebab_to_camel

from . import props
from .import_type_spec import import_type_spec
from .resources import DjangoModel

base_tags = {"module": ["django-module"]}


@create("django-model")
def create_django_model(term):
    django_model = DjangoModel(name=kebab_to_camel(term.data), kebab_name=term.data)
    return django_model


@extend(DjangoModel)
class ExtendDjangoModel:
    item_list = P.child(provides, "item~list")
    module = P.parent("module", has)
    form_field_spec = Prop(props.django_model_form_field_spec)


rules = {
    "module": {
        (contains + provides, "item~list"): empty_rule(),
        (has, "django-model"): empty_rule(),
    },
    "django-model": {
        (provides, "item~list"): (
            # base django_model on the type_spec of the item list
            lambda django_model, item_list: import_type_spec(
                item_list.item.type_spec, django_model
            )
        )
    },
}
