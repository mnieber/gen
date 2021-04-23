import moonleap.resource.props as P
from moonleap import MemFun, add, extend, kebab_to_camel, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_react.module import Module
from moonleap_react.nodepackage import load_node_package_config

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


@extend(Container)
class ExtendContainer:
    render = MemFun(render_templates(__file__))
    behaviors = P.children("has", "behavior")


@extend(Module)
class ExtendModule:
    container = P.child(has, "container")
