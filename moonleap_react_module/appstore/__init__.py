from moonleap import MemFun, Prop, extend, render_templates, tags

from . import props
from .resources import AppStore


@tags(["app:store"])
def create_appstore(term, block):
    store = AppStore(name="AppStore")
    return store


@extend(AppStore)
class ExtendAppStore:
    render = MemFun(render_templates(__file__))
    substores = Prop(props.substores)
