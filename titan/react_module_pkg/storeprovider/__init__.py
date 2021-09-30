from dataclasses import dataclass
from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, extend, rule
from moonleap.verbs import has
from titan.react_module_pkg.appmodule import AppModule
from titan.react_pkg.component import Component


@dataclass
class StoreProvider(Component):
    pass


base_tags = [("store-provider", ["component"])]


@create("store-provider")
def create_store_provider(term, block):
    store_provider = StoreProvider(name="StoreProvider")
    store_provider.add_template_dir(Path(__file__).parent / "templates")
    return store_provider


@rule("app:module")
def app_module_created(app_module):
    return create_forward(app_module, has, ":store-provider")


@extend(AppModule)
class ExtendAppModule:
    store_provider = P.child(has, "store-provider", required=True)
