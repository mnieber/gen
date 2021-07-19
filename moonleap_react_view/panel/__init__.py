import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, render_templates, rule, tags
from moonleap.verbs import shows

from . import props
from .resources import Panel


@tags(["panel"])
def create_panel(term, block):
    panel = Panel(name=f"{term.data}Panel", type=term.data)
    return panel


@rule("panel", shows, "children")
def panel_wraps_children(term, block):
    pass


def render(self, settings, output_root_dir, template_renderer):
    if self.collapses:
        return []

    return render_templates(__file__)(
        self, settings, output_root_dir, template_renderer
    )


@extend(Panel)
class ExtendPanel:
    render = MemFun(render)
    create_router_configs = MemFun(props.create_router_configs)
    root_component = Prop(props.root_component)
    wraps_children = P.child(shows, ":children")
    collapses = Prop(props.collapses)
