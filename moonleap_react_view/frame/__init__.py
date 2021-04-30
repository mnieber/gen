import moonleap.resource.props as P
from moonleap import (
    MemFun,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    upper0,
)
from moonleap.verbs import uses

from . import props
from .resources import Frame


@tags(["frame"])
def create_frame(term, block):
    name = kebab_to_camel(term.data)
    frame = Frame(name=f"{upper0(name)}Frame")
    return frame


@rule("frame")
def frame_created(frame):
    name = kebab_to_camel(frame.term.data)
    if [x for x in frame.module.states if x.name == name]:
        return create_forward(frame, uses, f"{name}:state-provider")


@extend(Frame)
class ExtendFrame:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
    state_provider = P.child(uses, "state-provider")
