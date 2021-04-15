import moonleap.resource.props as P
from moonleap import MemFun, extend, kebab_to_camel, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.module import Module

from .resources import Frame


@tags(["frame"])
def create_frame(term, block):
    name = kebab_to_camel(term.data)
    frame = Frame(basename=name, name=f"{name}Frame")
    return frame


@rule("module", has, "frame")
def module_has_frame(module, frame):
    frame.output_path = module.output_path
    frame.module = module
    return service_has_tool_rel(module.service, frame)


@extend(Frame)
class ExtendFrame:
    render = MemFun(render_templates(__file__))
