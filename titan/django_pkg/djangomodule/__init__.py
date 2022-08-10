from dataclasses import dataclass
from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    RenderMixin,
    Resource,
    TemplateDirMixin,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
from moonleap.verbs import contains, has, provides
from titan.api_pkg.itemlist import ItemList
from titan.api_pkg.itemtype.resources import ItemType
from titan.django_pkg.djangoapp import DjangoApp

from . import props


@dataclass
class DjangoModule(TemplateDirMixin, RenderMixin, Resource):
    name: str


rules = [
    (("module", contains + provides, "item~list"), empty_rule()),
]

base_tags = [("module", ["django-module"])]


@create("module")
def create_module(term):
    module = DjangoModule(name=kebab_to_camel(term.data))
    module.template_dir = Path(__file__).parent / "templates"
    module.template_context = dict(module=module)
    return module


@rule("django-app", has, "module")
def django_app_has_module(django_app, module):
    django_app.renders(
        module,
        module.name,
        module.template_context,
        [module.template_dir],
    )


@rule("module", contains + provides, "item~list")
def module_contains_item_list(module, item_list):
    django_model_term = f"{item_list.item_name}:django-model"
    return [
        create_forward(module, has, django_model_term),
        create_forward(django_model_term, provides, item_list),
    ]


@extend(DjangoModule)
class ExtendModule:
    item_lists_provided = P.children(provides, "item~list")
    django_models = P.children(has, "django-model")
    module_path = Prop(props.module_path)
    django_app = P.parent("django-app", has, required=True)


@extend(ItemList)
class ExtendItemList:
    django_module = P.parent("django-module", provides)


@extend(ItemType)
class ExtendItemType:
    django_module = Prop(props.item_type_django_module)


@extend(DjangoApp)
class ExtendDjangoApp:
    get_module_by_name = MemFun(props.get_module_by_name)
