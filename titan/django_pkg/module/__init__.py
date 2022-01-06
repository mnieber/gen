from pathlib import Path

import moonleap.resource.props as P
from moonleap import (
    Prop,
    StoreOutputPaths,
    StoreTemplateDirs,
    add,
    create,
    empty_rule,
    extend,
    kebab_to_camel,
    rule,
)
from moonleap.utils.case import kebab_to_camel, sn
from moonleap.verbs import contains, provides
from titan.django_pkg.djangoapp import StoreDjangoConfigs

from . import django_configs, props
from .get_context import get_context
from .get_context_admin import get_context_admin
from .get_context_test import get_context_test
from .resources import Module  # noqa

rules = [(("module", contains + provides, "item~list"), empty_rule())]

base_tags = [("module", ["django-module"])]


@create("module")
def create_module(term, block):
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


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreOutputPaths, StoreDjangoConfigs):
    item_lists_provided = P.children(provides, "item~list")
    module_path = Prop(props.module_path)
