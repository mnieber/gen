from moonleap import MemFun, RenderTemplates, extend

from . import props
from .resources import SelectItemEffect


@extend(SelectItemEffect)
class ExtendSelectItemEffect(RenderTemplates(__file__)):
    create_router_configs = MemFun(props.create_router_configs)
