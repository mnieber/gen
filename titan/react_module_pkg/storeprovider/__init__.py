from dataclasses import dataclass

import moonleap.resource.props as P
from moonleap import RenderTemplates, create_forward, extend, rule, tags
from moonleap.verbs import has
from titan.react_module_pkg.appmodule import AppModule
from titan.react_pkg.component import Component


@dataclass
class StoreProvider(Component):
    pass


@tags(["store-provider"])
def create_store_provider(term, block):
    store_provider = StoreProvider(name="StoreProvider")
    return store_provider


@rule("app:module")
def app_module_created(app_module):
    return create_forward(app_module, has, ":store-provider")


@extend(AppModule)
class ExtendAppModule:
    store_provider = P.child(has, "store-provider")


@extend(StoreProvider)
class ExtendStoreProvider(RenderTemplates(__file__)):
    pass
