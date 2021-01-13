import moonleap.props as P
import ramda as R
from leap_mn.layer import StoreLayerConfigs
from leap_mn.service import Service
from moonleap import extend, rule

from .props import get_makefile_rules, get_package_names
from .resources import Tool


@rule("service", "has", "*", fltr_obj=P.fltr_instance(Tool))
def service_has_tool(service, tool):
    service.add_to_tools(tool)
    service.add_to_layer_config_sources(tool)


@extend(Tool)
class ExtendTool(StoreLayerConfigs):
    pip_dependencies = P.children("has", ":pip-dependency")
    pip_dependencies_dev = P.children("has", "dev:pip-dependency")
    pkg_dependencies = P.children("has", ":pkg-dependency")
    pkg_dependencies_dev = P.children("has", "dev:pkg-dependency")
    makefile_rules = P.children("has", ":makefile-rule")


@extend(Service)
class ExtendService:
    tools = P.children("has", "tool")
    pip_dependencies = get_package_names("pip_dependencies")
    pip_dependencies_dev = get_package_names("pip_dependencies_dev")
    pkg_dependencies = get_package_names("pkg_dependencies")
    pkg_dependencies_dev = get_package_names("pkg_dependencies_dev")
    makefile_rules = get_makefile_rules()
