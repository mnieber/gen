import moonleap.resource.props as P
from moonleap import extend, rule, title0
from moonleap.verbs import has
from moonleap_react_view.frame.resources import Frame


@rule("frame", has, "panel")
def frame_has_panel(frame, panel):
    panel.output_paths.add_source(frame)
    panel.name = frame.item_name + title0(panel.type) + "Panel"
    panel.module = frame.module
    frame.dependencies.append(panel)


@extend(Frame)
class ExtendFrame:
    left_panel = P.child(has, "left:panel")
    right_panel = P.child(has, "right:panel")
    top_panel = P.child(has, "top:panel")
    bottom_panel = P.child(has, "bottom:panel")
