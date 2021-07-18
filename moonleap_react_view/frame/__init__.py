from moonleap import (
    MemFun,
    Prop,
    extend,
    kebab_to_camel,
    render_templates,
    tags,
    upper0,
)

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
    p_section_div = Prop(props.p_section_div)
    p_section_imports = Prop(props.p_section_imports)
