import moonleap.resource.props as P
from moonleap import Prop, Rel, extend, rule, tags, word_to_term
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.utils import title
from moonleap.verbs import contains, has
from moonleap_react.module import Module

from . import props
from .resources import Store


@tags(["store"])
def create_store(term, block):
    store = Store(name=f"{title(term.data)}Store", import_path="")
    store.add_template_dir(__file__, "templates")
    return store


@rule("module", has, "store")
def create_utils_module(module, store):
    return Rel(module.service.term, has, word_to_term("utils:module"))


@rule("module", has, "store")
def module_has_store(module, store):
    store.import_path = module.import_path + "/" + f"{store.name}"
    store.output_paths.add_source(module)
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(Module)
class ExtendModule:
    store = P.child(has, "store")


@extend(Store)
class ExtendStore(StoreTemplateDirs):
    module = P.parent(Module, has, "store")
    policy_lines = Prop(props.policy_lines)
    items = P.children(contains, "item")
    item_lists = P.children(contains, "item-list")
    item_types = P.children(contains, "item-type")
