from moonleap import MemFun, extend, kebab_to_camel, render_templates, tags

from . import props
from .resources import View


@tags(["view"])
def create_view(term, block):
    kebab_name = term.data
    name = kebab_to_camel(kebab_name)
    view = View(name=name + "View")
    return view


@extend(View)
class ExtendView:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
