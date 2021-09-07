from pathlib import Path

import moonleap.resource.props as P
from moonleap import MemFun, Prop, add, create, extend, register_add
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from titan.tools_pkg.pipdependency import PipRequirement

from . import (
    django_configs,
    docker_compose_configs,
    dodo_layer_configs,
    makefile_rules,
    opt_paths,
    props,
)
from .resources import DjangoApp, DjangoConfig


class StoreDjangoConfigs:
    django_configs = P.tree("p-has", "django_app-config")


@register_add(DjangoConfig)
def add_django_config(resource, django_config):
    resource.django_configs.add(django_config)


@create("django-app", ["tool"])
def create_django(term, block):
    django_app = DjangoApp(name="django-app")
    django_app.add_template_dir(Path(__file__).parent / "templates")
    add(django_app, django_configs.get())
    add(django_app, makefile_rules.get())
    add(django_app, dodo_layer_configs.get())
    add(django_app, opt_paths.static_opt_path)
    add(django_app, PipRequirement(["Django", "django-environ", "django-cors-headers"]))
    add(django_app, PipRequirement(["pytest-django", "django-extensions"], is_dev=True))
    add(django_app, docker_compose_configs.get(is_dev=True))
    add(django_app, docker_compose_configs.get(is_dev=False))
    return django_app


@extend(DjangoApp)
class ExtendDjangoApp(StoreTemplateDirs):
    config = Prop(props.config)
    get_setting_or = MemFun(props.get_setting_or)
    third_party_apps = Prop(props.third_party_apps)
    local_apps = Prop(props.local_apps)
    cors_urls_regex = Prop(props.cors_urls_regex)
    secret_key = Prop(props.secret_key)
