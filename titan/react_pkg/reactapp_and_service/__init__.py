import moonleap.resource.props as P
from moonleap import add, create_forward, extend, rule
from moonleap.verbs import has, runs, uses
from titan.project_pkg.service import Service

from . import dodo_layer_configs


@rule("service", runs, "react-app")
def service_uses_react_app(service, react_app):
    service.port = service.port or "3000"
    return [
        create_forward(service, has, ":makefile"),
        create_forward(service, has, ":node-package"),
        create_forward(service, uses, ":dodo-menu"),
    ]


@rule("service", uses, "dodo-menu")
def service_uses_dodo_menu(service, dodo_menu):
    add(dodo_menu, dodo_layer_configs.get_for_menu(service.name))


@extend(Service)
class ExtendService:
    react_app = P.child(runs, "react-app")
