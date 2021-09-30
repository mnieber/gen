from dataclasses import dataclass
from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, extend, kebab_to_camel
from moonleap.verbs import has
from titan.react_module_pkg.store import Store
from titan.react_pkg.component import Component


@dataclass
class Policy(Component):
    pass


base_tags = [("policy", ["component"])]


@create("policy")
def create_policy(term, block):
    name = kebab_to_camel(term.data)
    policy = Policy(name=name)
    policy.add_template_dir(Path(__file__).parent / "templates")
    return policy


@extend(Store)
class ExtendStore:
    policies = P.children(has, "policy")


@extend(Policy)
class ExtendPolicy:
    store = P.parent("react-store", has, required=True)
