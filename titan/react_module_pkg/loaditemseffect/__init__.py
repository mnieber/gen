from moonleap import MemFun, Prop, RenderTemplates, extend

from . import props
from .resources import LoadItemsEffect


@extend(LoadItemsEffect)
class ExtendLoadItemsEffect(RenderTemplates(__file__)):
    create_router_configs = MemFun(props.create_router_configs)
    sections = Prop(props.Sections)
