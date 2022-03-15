from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    Prop,
    StoreOutputPaths,
    StoreTemplateDirs,
    add,
    create,
    create_forward,
    empty_rule,
    extend,
    feeds,
    rule,
)
from moonleap.utils.case import kebab_to_camel, sn
from moonleap.verbs import contains, has, provides
from titan.django_pkg.djangoapp import StoreDjangoConfigs

from . import django_configs, props
from .get_context import get_context
from .get_context_admin import get_context_admin
from .get_context_test import get_context_test
from .resources import Module  # noqa

rules = [
    (("module", contains + provides, "item~list"), empty_rule()),
    (("module", has, "django-model"), feeds("output_paths")),
]

base_tags = [("module", ["django-module"])]


@create("module")
def create_module(term):
    module = Module(name=kebab_to_camel(term.data))
    module.output_path = sn(module.name)
    module.add_template_dir(Path(__file__).parent / "templates", get_context)
    module.add_template_dir(Path(__file__).parent / "templates_test", get_context_test)
    module.add_template_dir(
        Path(__file__).parent / "templates_admin", get_context_admin
    )
    return module


@rule("module")
def module_created(module):
    add(module, django_configs.get(module))


@rule("module", contains + provides, "item~list")
def module_contains_item_list(module, item_list):
    django_model_term = f"{item_list.item_name}:django-model"
    return [
        create_forward(module, has, django_model_term),
        create_forward(django_model_term, provides, item_list),
    ]


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreOutputPaths, StoreDjangoConfigs):
    item_lists_provided = P.children(provides, "item~list")
    django_models = P.children(has, "django-model")
    module_path = Prop(props.module_path)
