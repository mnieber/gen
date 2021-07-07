import moonleap.resource.props as P
from moonleap import MemFun, extend, kebab_to_camel, render_templates, tags, upper0
from moonleap.verbs import uses

from . import props
from .resources import Frame


@tags(["frame"])
def create_frame(term, block):
    name = kebab_to_camel(term.data)
    frame = Frame(name=f"{upper0(name)}Frame")
    return frame


@extend(Frame)
class ExtendFrame:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
