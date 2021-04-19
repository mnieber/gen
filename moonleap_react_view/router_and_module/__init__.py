import moonleap.resource.props as P
from moonleap import MemFun, extend
from moonleap.verbs import has
from moonleap_react.component import Component
from moonleap_react_module.appmodule import AppModule
from moonleap_react_view.router import StoreRouterConfigs


@extend(AppModule)
class ExtendAppModule:
    router = P.child(has, "router")


@extend(Component)
class ExtendComponent(StoreRouterConfigs):
    create_router_configs = MemFun(lambda x: None)
