from dataclasses import dataclass

import moonleap.resource.props as P
from leapreact.appmodule import AppModule
from leapreact.component import Component
from moonleap import Prop, Resource, StoreOutputPaths, created, extend, render_templates
from moonleap.verbs import has

from . import props


@dataclass
class StoreProvider(Component):
    pass


@created("app:module")
def app_module_created(app_module):
    store_provider = StoreProvider(name="StoreProvider", import_path="src/app")
    store_provider.output_paths.add_source(app_module)
    app_module.store_provider = store_provider


@extend(AppModule)
class ExtendAppModule:
    store_provider = P.child(has, "store-provider")


@extend(StoreProvider)
class ExtendStoreProvider(StoreOutputPaths):
    render = render_templates(__file__)
    app_module = P.parent(AppModule, has, "store-provider")
    policy_lines = Prop(props.policy_lines)
    substores = Prop(props.substores)
