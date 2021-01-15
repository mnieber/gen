import moonleap.props as P
import ramda as R
from leap_mn.layer import StoreLayerConfigs
from leap_mn.optpath import StoreOptPaths
from leap_mn.outputpath import StoreOutputPaths
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
    tool.output_paths.add_source(service)


class StoreDependencies:
    pip_dependencies = P.tree(
        "has", "pip-dependency", merge=lambda acc, x: [*acc, x], initial=list()
    )
    pkg_dependencies = P.tree(
        "has", "pkg-dependency", merge=lambda acc, x: [*acc, x], initial=list()
    )


@extend(Tool)
class ExtendTool(StoreLayerConfigs, StoreOptPaths, StoreDependencies, StoreOutputPaths):
    makefile_rules = P.children("has", "makefile-rule")


@extend(Service)
class ExtendService:
    tools = P.children(("has", "uses"), "tool")
    get_pkg_names = MemFun(props.get_pkg_names())
    get_pip_pkg_names = MemFun(props.get_pip_pkg_names())
    makefile_rules = Prop(props.get_makefile_rules())
