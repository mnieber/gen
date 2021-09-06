from moonleap import extend
from titan.project_pkg.service import Tool
from titan.react_pkg.component import Component
from titan.react_pkg.module import Module
from titan.react_pkg.reactapp import StoreReactAppConfigs


@extend(Tool)
class ExtendTool(StoreReactAppConfigs):
    pass


@extend(Component)
class ExtendComponent(StoreReactAppConfigs):
    pass


@extend(Module)
class ExtendModule(StoreReactAppConfigs):
    pass
