import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, extend, register_add, tags
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has
from moonleap_project.service import Tool
from moonleap_tools.pipdependency import PipRequirement

from . import docker_compose_configs, layer_configs, makefile_rules, opt_paths, props
from .resources import Django, DjangoConfig


@tags(["django"])
def create_django(term, block):
    django = Django(name="django")
    django.add_template_dir(__file__, "templates")
    add(django, makefile_rules.get())
    add(django, layer_configs.get())
    add(django, opt_paths.static_opt_path)
    add(django, PipRequirement(["Django"]))
    add(django, docker_compose_configs.get(is_dev=True))
    add(django, docker_compose_configs.get(is_dev=False))
    return django


class StoreDjangoConfigs:
    django_configs = P.tree(has, "django-config")


@register_add(DjangoConfig)
def add_django_config(resource, django_config):
    resource.django_configs.add(django_config)


@extend(Django)
class ExtendDjango(StoreTemplateDirs):
    settings = Prop(props.settings)
    get_settings_or = MemFun(props.get_settings_or)


@extend(Tool)
class ExtendTool(StoreDjangoConfigs):
    pass
