import moonleap.resource.props as P
from moonleap import Prop, RenderTemplates, extend, tags
from moonleap.verbs import has
from titan.react_module_pkg.appmodule import AppModule

from . import props
from .resources import AppStore


@tags(["app:store"])
def create_appstore(term, block):
    store = AppStore(name="AppStore")
    return store


@extend(AppStore)
class ExtendAppStore(RenderTemplates(__file__)):
    substores = Prop(props.substores)


@extend(AppModule)
class ExtendModule:
    app_store = P.child(has, "app:store")
