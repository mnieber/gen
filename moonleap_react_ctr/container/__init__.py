import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    add,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
)
from moonleap.verbs import has, with_
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import Container


@tags(["container"])
def create_container(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    container = Container(name=name)
    add(container, load_node_package_config(__file__))
    return container


@rule("module", has, "container")
def module_has_container(module, container):
    container.output_paths.add_source(module)
    module.service.utils_module.add_template_dir(__file__, "templates_utils")


@extend(Container)
class ExtendContainer:
    render = MemFun(render_templates(__file__))
    behaviors = P.children(has + with_, "behavior")
    declare_policies_section = Prop(props.declare_policies_section)
    policies_section = Prop(props.policies_section)


@extend(Module)
class ExtendModule:
    container = P.child(has, "container")
