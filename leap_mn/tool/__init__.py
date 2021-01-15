import moonleap.props as P
import ramda as R
from leap_mn.layer import StoreLayerConfigs
from leap_mn.optpath import StoreOptPaths
from leap_mn.service import Service
from moonleap import extend, rule
from moonleap.memfun import MemFun
from moonleap.prop import Prop

from . import props
from .resources import Tool


@rule("service", ("has", "uses"), "*", fltr_obj=P.fltr_instance(Tool))
def service_has_tool(service, tool):
    service.add_to_tools(tool)
    service.layer_configs.add_source(tool)


@extend(Tool)
class ExtendTool(StoreLayerConfigs, StoreOptPaths):
    pip_dependencies = P.children("has", "pip-dependency")
    pkg_dependencies = P.children("has", "pkg-dependency")
    makefile_rules = P.children("has", "makefile-rule")


@extend(Service)
class ExtendService:
    tools = P.children(("has", "uses"), "tool")
    get_pip_dependencies = MemFun(props.get_package_names("pip_dependencies"))
    get_pkg_dependencies = MemFun(props.get_package_names("pkg_dependencies"))
    makefile_rules = Prop(props.get_makefile_rules())
