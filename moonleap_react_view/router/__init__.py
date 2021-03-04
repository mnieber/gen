import moonleap.resource.props as P
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config
from moonleap_react_module.appmodule import AppModule
from moonleap_tools.tool import Tool

from . import props
from .resources import Router


@tags(["router"])
def create_router(term, block):
    router = Router(name="UrlRouter")
    add(router, load_node_package_config(__file__))
    return router


@rule("app:module", has, "router")
def service_has_router(app_module, router):
    router.output_path = app_module.output_path
    app_module.service.add_tool(router)


@extend(Router)
class ExtendRouter:
    module = P.parent(Module, has, "router")
    get_item_types = MemFun(props.get_item_types)
    has_list_view = MemFun(props.has_list_view)
    has_form_view = MemFun(props.has_form_view)
    get_imports = MemFun(props.get_imports)
    render = MemFun(render_templates(__file__))


class StoreRouterConfigs:
    router_configs = P.tree("has", "router-config")


@extend(Tool)
class ExtendTool(StoreRouterConfigs):
    pass


@extend(AppModule)
class ExtendAppModule:
    router = P.child(has, "router")
