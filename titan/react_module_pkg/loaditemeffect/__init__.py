from moonleap import MemFun, Prop, RenderTemplates, extend

from . import props
from .resources import LoadItemEffect


@extend(LoadItemEffect)
class ExtendLoadItemEffect(RenderTemplates(__file__)):
    sections = Prop(props.Sections)
    create_router_configs = MemFun(props.create_router_configs)
