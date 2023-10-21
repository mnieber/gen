from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import (
    MemFun,
    Prop,
    create,
    create_forward,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
from moonleap.blocks.verbs import contains, has, provides
from moonleap.utils.case import sn
from titan.django_pkg.djangoapp import DjangoApp
from titan.django_pkg.djangomodule.get_map_from_item_to_django_module import (
    get_map_from_item_to_django_module,
)
from titan.types_pkg.item import Item
from titan.types_pkg.itemlist import ItemList
from titan.types_pkg.typeregistry import get_type_reg
from titan.typespec.type_spec import TypeSpec

from . import props
from .resources import DjangoModule

base_tags = {"module": ["django-module"]}


def create_django_module(klass, term, template_dir, has_graphql_schema=False):
    module = klass(name=kebab_to_camel(term.data), kebab_name=term.data)
    module.template_dir = template_dir
    module.template_context = dict(module=module)
    module.has_graphql_schema = has_graphql_schema
    return module


@create("module")
def create_module(term):
    return create_django_module(DjangoModule, term, Path(__file__).parent / "templates")


@create("user-accounts:module")
def create_accounts_module(term):
    return create_django_module(
        DjangoModule,
        term,
        Path(__file__).parent / "templates_user_accounts",
        has_graphql_schema=True,
    )


@create("users:module")
def create_users_module(term):
    return create_django_module(
        DjangoModule, term, Path(__file__).parent / "templates_users"
    )


def django_app_renders_module(django_app, module):
    django_app.renders(
        [module],
        sn(module.name),
        module.template_context,
        [module.template_dir],
    )


@rule("django-app")
def django_modules_provide_item_lists(django_app):
    lut = get_map_from_item_to_django_module(get_type_reg(), django_app.modules)
    forwards = []
    for data in lut.values():
        if not data.item.type_spec.only_api:
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


@extend(TypeSpec)
class ExtendTypeSpec:
    django_module = Prop(props.type_spec_django_module)


@extend(DjangoApp)
class ExtendDjangoApp:
    modules = P.children(
        has, "module", lambda modules: sorted(modules, key=lambda x: x.name)
    )
    user_accounts_module = P.child(has, "user-accounts:module")
    get_module_by_name = MemFun(props.get_module_by_name)


rules = {
    "module": {
        (contains + provides, "item~list"): empty_rule(),
    },
    "django-app": {
        (has, "module"): (
            #
            django_app_renders_module
        )
    },
}
