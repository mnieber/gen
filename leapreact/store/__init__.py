import moonleap.resource.props as P
from leapreact.module import Module
from leapreact.utilsmodule import create_utils_module
from moonleap import MemFun, Prop, extend, render_templates, rule, tags
from moonleap.verbs import contains, has

from . import props
from .render import render
from .resources import Store


@tags(["store"])
def create_store(term, block):
    store = Store(name=f"{term.data.title()}Store", import_path="")
    return store


@rule("module", has, "store")
def module_has_store(module, store):
    store.import_path = module.import_path + "/" + f"{store.name}"
    store.output_paths.add_source(module)
    utils_module = create_utils_module(module.service)
    utils_module.add_template_dir(__file__, "templates_utils")


@extend(Module)
class ExtendModule:
    store = P.child(has, "store")


@extend(Store)
class ExtendStore:
    render = MemFun(render)
    module = P.parent(Module, has, "store")
    policy_lines = Prop(props.policy_lines)
    item_lists = P.children(contains, "item-list")
