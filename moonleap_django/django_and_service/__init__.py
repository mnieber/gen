import moonleap.resource.props as P
from moonleap import add, add_source, create_forward, extend, rule
from moonleap.verbs import has, runs, uses
from moonleap_django.django import StoreDjangoConfigs
from moonleap_django.django.resources import Django
from moonleap_project.service import Service

from . import layer_configs


@rule("service", has, "tool")
def service_has_tool(service, tool):
    add_source(
        [service, "django_configs"],
        tool,
        "The :service receives django configs from a :tool",
    )


@rule("service", uses + runs, "django")
def service_has_django(service, django):
    service.port = service.port or "8000"
    add(service.project, layer_configs.get(service.name))
    django.django_configs.add_source(service)
    return create_forward(service, has, ":makefile")


@extend(Django)
class ExtendDjango:
    service = P.parent(Service, uses + runs)


@extend(Service)
class ExtendService(StoreDjangoConfigs):
    pass
