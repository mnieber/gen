import moonleap.resource.props as P
from moonleap import Prop, extend, tags
from moonleap.verbs import has, with_
from moonleap_react.nodepackage import StoreNodePackageConfigs
from moonleap_react_ctr.container.resources import Container

from . import props
from .resources import Behavior


@tags(["behavior"])
def create_behavior(term, block):
    behavior = Behavior(name=term.data)
    return behavior


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    container = P.parent(Container, has + with_, "behavior")

    imports_section = Prop(props.imports_section)
    constructor_section = Prop(props.constructor_section)
    callbacks_section = Prop(props.callbacks_section)
    declare_policies_section = Prop(props.declare_policies_section)
    policies_section = Prop(props.policies_section)
