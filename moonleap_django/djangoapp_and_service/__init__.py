import moonleap.resource.props as P
from moonleap import add, add_source, create_forward, extend, rule
from moonleap.verbs import has, runs
from moonleap_django.djangoapp import StoreDjangoConfigs
from moonleap_django.djangoapp.resources import DjangoApp
from moonleap_project.service import Service, Tool

from . import layer_configs


@rule("service", has, "tool")
def service_has_tool(service, tool):
    add_source(
        [service, "django_configs"],
        tool,
        "The :service receives django configs from a :tool",
    )


@rule("service", runs, "django-app")
def service_runs_django_app(service, django_app):
    service.port = service.port or "8000"
    add(service.project, layer_configs.get(service.name))
    django_app.django_configs.add_source(service)
    return [
        create_forward(service, has, ":makefile"),
        create_forward(django_app, has, "app:module"),
    ]


@extend(DjangoApp)
class ExtendDjangoApp:
    service = P.parent(Service, runs)


@extend(Service)
class ExtendService(StoreDjangoConfigs):
    django_app = P.child(runs, ":django-app")


@extend(Tool)
class ExtendTool(StoreDjangoConfigs):
    pass
