import moonleap.resource.props as P
from moonleap import Prop, create_forward, extend, rule, tags
from moonleap.verbs import has, supports
from moonleap_react.nodepackage import StoreNodePackageConfigs
from moonleap_react_ctr.container.resources import Container

from . import props
from .resources import Behavior


@tags(["behavior"])
def create_behavior(term, block):
    behavior = Behavior(name=term.data)
    return behavior


@rule("container", supports, "*", fltr_obj=P.fltr_instance(Behavior))
def container_supports_a_behavior(container, behavior):
    __import__("pudb").set_trace()
    return create_forward(container, has, ":behavior", obj_res=behavior)


@extend(Behavior)
class ExtendBehavior(StoreNodePackageConfigs):
    container = P.parent(Container, supports, "behavior")

    imports_section = Prop(props.imports_section)
    constructor_section = Prop(props.constructor_section)
    callbacks_section = Prop(props.callbacks_section)
    declare_policies_section = Prop(props.declare_policies_section)
    policies_section = Prop(props.policies_section)
