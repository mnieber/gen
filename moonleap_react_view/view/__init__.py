import moonleap.resource.props as P
from moonleap import (
    MemFun,
    Prop,
    create_forward,
    extend,
    kebab_to_camel,
    render_templates,
    rule,
    tags,
    upper0,
)
from moonleap.verbs import has

from . import props
from .resources import View


@tags(["view"])
def create_view(term, block):
    kebab_name = term.data
    view = View(name=upper0(kebab_to_camel(kebab_name)))
    return view


@rule("view", has, "panel")
def view_has_panel(view, panel):
    panel.name = view.name + upper0(panel.type) + "Panel"
    return create_forward(view.module, has, ":component", panel)


@extend(View)
class ExtendView:
    left_panel = P.child(has, "left:panel")
    right_panel = P.child(has, "right:panel")
    top_panel = P.child(has, "top:panel")
    bottom_panel = P.child(has, "bottom:panel")
    middle_panel = P.child(has, "middle:panel")
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
    p_section_div = Prop(props.p_section_div)
    p_section_imports = Prop(props.p_section_imports)
