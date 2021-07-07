import moonleap.resource.props as P
from moonleap import MemFun, Prop, extend, render_templates, tags
from moonleap.verbs import has
from moonleap_react_module.appmodule import AppModule

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


@extend(AppModule)
class ExtendModule:
    app_store = P.child(has, "app:store")
