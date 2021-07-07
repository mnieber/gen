from moonleap import MemFun, extend, render_templates

from . import props
from .resources import SelectItemEffect


@extend(SelectItemEffect)
class ExtendSelectItemEffect:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
