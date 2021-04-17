from moonleap import MemFun, extend, kebab_to_camel, render_templates, tags

from .resources import Frame


@tags(["frame"])
def create_frame(term, block):
    name = kebab_to_camel(term.data)
    frame = Frame(item_type_name=name, name=f"{name}Frame")
    return frame


@extend(Frame)
class ExtendFrame:
    render = MemFun(render_templates(__file__))
