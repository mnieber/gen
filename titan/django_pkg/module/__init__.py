from moonleap import (
    MemFun,
    StoreOutputPaths,
    add,
    extend,
    kebab_to_camel,
    kebab_to_snake,
    rule,
    tags,
)
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from titan.django_pkg.djangoapp import StoreDjangoConfigs

from . import django_configs, props
from .resources import Module  # noqa


@tags(["module"])
def create_module(term, block):
    name = kebab_to_camel(term.data)
    name_snake = kebab_to_snake(term.data)
    module = Module(name_snake=name_snake, name=name)
    module.output_path = module.name_snake
    module.add_template_dir(__file__, "templates")
    return module


@rule("module")
def module_created(module):
    add(module, django_configs.get(module))


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreOutputPaths, StoreDjangoConfigs):
    p_section_model_fields = MemFun(props.p_section_model_fields)
