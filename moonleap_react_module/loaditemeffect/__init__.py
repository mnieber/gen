from moonleap import MemFun, Prop, extend, render_templates

from . import props
from .resources import LoadItemEffect


@extend(LoadItemEffect)
class ExtendLoadItemEffect:
    render = MemFun(render_templates(__file__))
    effect_section = Prop(props.effect_section)
    create_router_configs = MemFun(props.create_router_configs)
