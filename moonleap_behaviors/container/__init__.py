from moonleap import MemFun, extend, kebab_to_camel, render_templates, tags

from .resources import Container


@tags(["container"])
def create_container(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    container = Container(name=name)
    return container


@extend(Container)
class ExtendContainer:
    render = MemFun(render_templates(__file__))
