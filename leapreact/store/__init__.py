import moonleap.resource.props as P
from leapreact.module import Module
from moonleap import Prop, Resource, StoreOutputPaths, created, extend, render_templates
from moonleap.verbs import has

from . import props
from .resources import Store


@created("module")
def module_created(module):
    if module.name != "app":
        store = Store(
            name=f"{module.name.title()}Store", import_path=module.import_path
        )
        store.output_paths.add_source(module)
        module.store = store


@extend(Module)
class ExtendModule:
    store = P.child(has, "store")


@extend(Store)
class ExtendStore:
    render = render_templates(__file__)
    module = P.parent(Module, has, "store")
