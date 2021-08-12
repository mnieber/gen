import moonleap.resource.props as P
from moonleap import MemFun, extend
from moonleap.verbs import has
from titan.react_pkg.component import Component
from titan.react_module_pkg.appmodule import AppModule
from titan.react_view_pkg.router import StoreRouterConfigs


@extend(AppModule)
class ExtendAppModule:
    router = P.child(has, "router")


@extend(Component)
class ExtendComponent(StoreRouterConfigs):
    create_router_configs = MemFun(lambda x: None)
