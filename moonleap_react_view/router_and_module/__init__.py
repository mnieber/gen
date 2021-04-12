import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.module import Module
from moonleap_react_module.appmodule import AppModule
from moonleap_react_view.router.resources import Router


@rule("app:module", has, "router")
def service_has_router(app_module, router):
    router.output_path = app_module.output_path
    return service_has_tool_rel(app_module.service, router)


@extend(Router)
class ExtendRouter:
    module = P.parent(Module, has, "router")


@extend(AppModule)
class ExtendAppModule:
    router = P.child(has, "router")
