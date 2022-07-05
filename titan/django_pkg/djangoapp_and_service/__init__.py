import moonleap.resource.props as P
from moonleap import add, create_forward, extend, feeds, receives, rule
from moonleap.verbs import has, runs
from titan.django_pkg.djangoapp import StoreDjangoConfigs
from titan.project_pkg.service import Service, Tool

from . import dodo_layer_configs

rules = [
    (("service", has + runs, "tool"), receives("django_configs")),
    (("service", runs, "django-app"), feeds("django_configs")),
]


@rule("service", runs, "django-app")
def service_runs_django_app(service, django_app):
    service.port = service.port or "8000"
    add(service.project, dodo_layer_configs.get_for_project(service.name))
    return [
        create_forward(service, has, ":makefile"),
        create_forward(django_app, has, "app:module"),
    ]


@extend(Service)
class ExtendService(StoreDjangoConfigs):
    django_app = P.child(runs, ":django-app")


@extend(Tool)
class ExtendTool(StoreDjangoConfigs):
    pass
