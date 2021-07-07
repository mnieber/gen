import moonleap.resource.props as P
from moonleap import create_forward, extend, rule, upper0
from moonleap.verbs import has
from moonleap_react_view.frame.resources import Frame


@rule("frame", has, "panel")
def frame_has_panel(frame, panel):
    panel.name = frame.name + upper0(panel.type) + "Panel"
    frame.dependencies.append(panel)
    return create_forward(frame.module, has, ":component", panel)


@extend(Frame)
class ExtendFrame:
    left_panel = P.child(has, "left:panel")
    right_panel = P.child(has, "right:panel")
    top_panel = P.child(has, "top:panel")
    bottom_panel = P.child(has, "bottom:panel")
