from dataclasses import dataclass

import moonleap.resource.props as P
from moonleap import RenderTemplates, create_forward, extend, kebab_to_camel, rule, tags
from moonleap.verbs import has
from titan.react_module_pkg.store import Store
from titan.react_pkg.component import Component


@dataclass
class Policy(Component):
    pass


@tags(["policy"])
def create_policy(term, block):
    name = kebab_to_camel(term.data)
    policy = Policy(name=name)
    return policy


@rule("store", has, "policy")
def store_has_policy(store, policy):
    return create_forward(store.module, has, ":component", policy)


@extend(Store)
class ExtendStore:
    policies = P.children(has, "policy")


@extend(Policy)
class ExtendPolicy(RenderTemplates(__file__)):
    store = P.parent(Store, has)
