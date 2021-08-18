from moonleap import MemFun, Prop, extend, render_templates

from . import props
from .resources import LoadItemEffect


@extend(LoadItemEffect)
class ExtendLoadItemEffect:
    render = MemFun(render_templates(__file__))
    p_section_effect = Prop(props.p_section_effect)
    p_section_effect_args = Prop(props.p_section_effect_args)
    create_router_configs = MemFun(props.create_router_configs)
