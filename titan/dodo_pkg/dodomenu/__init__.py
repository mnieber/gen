from moonleap import create, extend, receives
from moonleap.verbs import contains
from titan.dodo_pkg.layer import StoreLayerConfigs

from .resources import DodoMenu

rules = [(("layer", contains, "dodo-menu"), receives("dodo_layer_configs"))]


@create("dodo-menu")
def create_layer(term):
    dodo_menu = DodoMenu()
    return dodo_menu


@extend(DodoMenu)
class ExtendDodoMenu(StoreLayerConfigs):
    pass
