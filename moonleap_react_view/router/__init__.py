import moonleap.resource.props as P
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_react.component import Component
from moonleap_react.module import Module
from moonleap_react_module.appmodule import AppModule

from . import node_package_configs, props


class Router(Component):
    pass


@tags(["router"])
def create_router(term, block):
    router = Router(name="UrlRouter", import_path="")
    add(router, node_package_configs.get())
    return router


@rule("app:module", has, "router")
def service_has_router(app_module, router):
    router.output_path = app_module.output_path
    app_module.service.add_tool(router)


@extend(Router)
class ExtendRouter:
    module = P.parent(Module, has, "router")
    get_views = MemFun(props.get_views)
    render = MemFun(render_templates(__file__))


@extend(AppModule)
class ExtendAppModule:
    router = P.child(has, "router")
