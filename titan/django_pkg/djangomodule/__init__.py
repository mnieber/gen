from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Priorities,
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
from moonleap.utils.case import sn
from moonleap.verbs import contains, has, provides
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.djangomodule.get_map_from_item_to_django_module import (
    get_map_from_item_to_django_module,
)
from titan.types_pkg.item.resources import Item
from titan.types_pkg.itemlist import ItemList

from . import props
from .resources import DjangoModule

rules = {
    ("module", contains + provides, "item~list"): empty_rule(),
}

base_tags = {"module": ["django-module"]}


@create("module")
def create_module(term):
    module = DjangoModule(name=kebab_to_camel(term.data), kebab_name=term.data)
    module.template_dir = Path(__file__).parent / "templates"
    module.template_context = dict(module=module)
    return module


@create("accounts:module")
def create_accounts_module(term):
    module = DjangoModule(name=kebab_to_camel(term.data), kebab_name=term.data)
    module.template_dir = Path(__file__).parent / "templates_accounts"
    module.template_context = dict(module=module)
    module.has_graphql_schema = True
    return module


@create("users:module")
def create_users_module(term):
    module = DjangoModule(name=kebab_to_camel(term.data), kebab_name=term.data)
    module.template_dir = Path(__file__).parent / "templates_users"
    module.template_context = dict(module=module)
    return module


@rule("django-app", has, "module")
def django_app_has_module(django_app, module):
    django_app.renders(
        [module],
        sn(module.name),
        module.template_context,
        [module.template_dir],
    )


@rule("django-app", priority=Priorities.LOW.value)
def django_modules_provide_item_lists(django_app):
    lut = get_map_from_item_to_django_module(django_app.modules)
    forwards = []
    for data in lut.values():
        django_model_term = f"{data.item.meta.term.data}:django-model"
        forwards.extend(
            [
                create_forward(data.django_module, provides, data.item.item_list),
                create_forward(data.django_module, has, django_model_term),
                create_forward(django_model_term, provides, data.item.item_list),
            ]
        )
    return forwards


@extend(DjangoModule)
class ExtendModule:
    django_models = P.children(has, "django-model")
    item_lists_provided = P.children(contains + provides, "item~list")
    module_path = Prop(props.module_path)
    django_app = P.parent("django-app", has, required=True)


@extend(ItemList)
class ExtendItemList:
    django_module = P.parent("django-module", contains + provides)


@extend(Item)
class ExtendItem:
    django_module = Prop(props.item_django_module)


@extend(DjangoApp)
class ExtendDjangoApp:
    modules = P.children(
        has, "module", lambda modules: sorted(modules, key=lambda x: x.name)
    )
    accounts_module = P.child(has, "accounts:module")
    get_module_by_name = MemFun(props.get_module_by_name)
