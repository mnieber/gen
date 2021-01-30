from moonleap import Prop, extend, render_templates, tags

from . import props
from .resources import AppStore


@tags(["app:store"])
def create_appstore(term, block):
    store = AppStore(name="AppStore", import_path="")
    return store


@extend(AppStore)
class ExtendAppStore:
    render = render_templates(__file__)
    substores = Prop(props.substores)
