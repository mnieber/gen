from pathlib import Path

import moonleap.resource.props as P
from moonleap import Prop, create, extend
from moonleap.verbs import has
from titan.react_module_pkg.appmodule import AppModule

from . import props
from .resources import AppStore


@create("app:store", ["component"])
def create_appstore(term, block):
    store = AppStore(name="AppStore")
    store.add_template_dir(Path(__file__).parent / "templates")
    return store


@extend(AppStore)
class ExtendAppStore:
    substores = Prop(props.substores)


@extend(AppModule)
class ExtendModule:
    app_store = P.child(has, "app:store")
