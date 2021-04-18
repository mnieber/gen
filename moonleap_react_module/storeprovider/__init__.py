from dataclasses import dataclass

import moonleap.resource.props as P
from moonleap import (
    MemFun,
    StoreOutputPaths,
    create_forward,
    extend,
    render_templates,
    rule,
    tags,
)
from moonleap.verbs import has
from moonleap_react.component import Component
from moonleap_react.module import module_has_component_rel
from moonleap_react_module.appmodule import AppModule


@dataclass
class StoreProvider(Component):
    pass


@tags(["store-provider"])
def create_store_provider(block, term):
    store_provider = StoreProvider(name="StoreProvider")
    return store_provider


@rule("app:module")
def app_module_created(app_module):
    return create_forward(app_module, has, ":store-provider")


@extend(AppModule)
class ExtendAppModule:
    store_provider = P.child(has, "store-provider")


@extend(StoreProvider)
class ExtendStoreProvider(StoreOutputPaths):
    render = MemFun(render_templates(__file__))
    app_module = P.parent(AppModule, has, "store-provider")
