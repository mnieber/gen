from moonleap import MemFun, extend, render_templates

from . import props
from .resources import LoadItemsEffect


@extend(LoadItemsEffect)
class ExtendLoadItemsEffect:
    render = MemFun(render_templates(__file__))
    create_router_configs = MemFun(props.create_router_configs)
