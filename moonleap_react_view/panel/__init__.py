import moonleap.resource.props as P
from moonleap import (
    MemFun,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    title0,
)
from moonleap.resources.outputpath.props import output_path
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react_view.frame.resources import Frame

from .resources import Panel


@tags(["panel"])
def create_panel(term, block):
    panel = Panel(name=f"{term.data}Panel", type=term.data)
    return panel


@rule("frame", has, "panel")
def frame_has_panel(frame, panel):
    panel.output_paths.add_source(frame)
    panel.name = frame.basename + title0(panel.type) + "Panel"
    panel.module = frame.module
    frame.dependencies.append(panel)
    return frame


@extend(Frame)
class ExtendFrame:
    left_panel = P.child(has, "left:panel")
    right_panel = P.child(has, "right:panel")
    top_panel = P.child(has, "top:panel")
    bottom_panel = P.child(has, "bottom:panel")


@extend(Panel)
class ExtendPanel:
    frame = P.parent(Frame, has, "panel")
