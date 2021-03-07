import moonleap.resource.props as P
from moonleap import MemFun, extend, kebab_to_camel, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_react.module import Module

from .resources import Container


@tags(["container"])
def create_container(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    container = Container(name=name)
    return container


@rule("module", has, "container")
def module_has_container(module, container):
    container.output_paths.add_source(module)


@extend(Container)
class ExtendListView:
    render = MemFun(render_templates(__file__))
    module = P.parent(Module, has, "container")
