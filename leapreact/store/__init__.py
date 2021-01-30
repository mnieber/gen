import moonleap.resource.props as P
from leapreact.module import Module
from moonleap import Prop, extend, render_templates, rule, tags
from moonleap.verbs import has

from . import props
from .resources import Store


@tags(["store"])
def create_store(term, block):
    store = Store(name=f"{term.data.title()}Store", import_path="")
    return store


@rule("module", has, "store")
def module_has_store(module, store):
    store.import_path = module.import_path + "/" + f"{store.name}"
    store.output_paths.add_source(module)


@extend(Module)
class ExtendModule:
    store = P.child(has, "store")


@extend(Store)
class ExtendStore:
    render = render_templates(__file__)
    module = P.parent(Module, has, "store")
    policy_lines = Prop(props.policy_lines)
