import moonleap.resource.props as P
from moonleap import add, extend, rule
from moonleap.verbs import has
from moonleap_react.component import Component
from moonleap_react.module import Module
from moonleap_react_module.appmodule import AppModule
from moonleap_react_view.router import RouterConfig, StoreRouterConfigs


@rule("*", has, "route", fltr_subj=P.fltr_instance(Component))
def component_has_route(component, route):
    add(
        component.module,
        RouterConfig(component=component),
        "The :component has a router config",
    )


@extend(AppModule)
class ExtendAppModule:
    router = P.child(has, "router")


@extend(Module)
class ExtendModule(StoreRouterConfigs):
    pass
