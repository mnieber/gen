from moonleap import MemFun, StoreOutputPaths, add, extend, kebab_to_snake, rule, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils.case import snake_to_camel
from moonleap_django.djangoapp import StoreDjangoConfigs

from . import django_configs, props
from .resources import Module  # noqa


@tags(["module"])
def create_module(term, block):
    name_snake = kebab_to_snake(term.data)
    module = Module(name_snake=name_snake, name_camel=snake_to_camel(name_snake))
    module.output_path = module.name_snake
    module.add_template_dir(__file__, "templates")
    return module


@rule("module")
def module_created(module):
    add(module, django_configs.get(module))


@extend(Module)
class ExtendModule(StoreTemplateDirs, StoreOutputPaths, StoreDjangoConfigs):
    p_section_fields = MemFun(props.p_section_fields)
