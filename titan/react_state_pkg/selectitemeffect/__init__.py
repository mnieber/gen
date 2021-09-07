from moonleap import MemFun, extend

from . import props
from .resources import SelectItemEffect


@extend(SelectItemEffect)
class ExtendSelectItemEffect:
    create_router_configs = MemFun(props.create_router_configs)
