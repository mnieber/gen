import moonleap.resource.props as P
from moonleap import MemFun, extend, rule, tags
from moonleap.verbs import has
from moonleap_react.component import Component
from moonleap_react_view.frame.resources import Frame

from . import props
from .resources import Panel


@tags(["panel"])
def create_panel(term, block):
    panel = Panel(name=f"{term.data}Panel", type=term.data)
    return panel


@extend(Panel)
class ExtendPanel:
    frame = P.parent(Frame, has, "panel")
    create_router_configs = MemFun(props.create_router_configs)
