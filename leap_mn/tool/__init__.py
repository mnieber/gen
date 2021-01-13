import moonleap.props as P
import ramda as R
from moonleap.config import extend, rule

from .props import get_makefile_rules, get_package_names
from .resources import Tool


@rule("service", "has", "*", fltr_obj=P.fltr_instance(Tool))
def service_has_tool(service, tool):
    service.add_to_tools(tool)


def meta():
    from leap_mn.service import Service

    @extend(Tool)
    class ExtendTool:
        pip_dependencies = P.children("has", ":pip-dependency")
        pip_dependencies_dev = P.children("has", "dev:pip-dependency")
        pkg_dependencies = P.children("has", ":pkg-dependency")
        pkg_dependencies_dev = P.children("has", "dev:pkg-dependency")
        makefile_rules = P.children("has", ":makefile-rule")
        layer_config = P.child("has", "layer-config")

    @extend(Service)
    class ExtendService:
        tools = P.children("has", "tool")
        pip_dependencies = get_package_names("pip_dependencies")
        pip_dependencies_dev = get_package_names("pip_dependencies_dev")
        pkg_dependencies = get_package_names("pkg_dependencies")
        pkg_dependencies_dev = get_package_names("pkg_dependencies_dev")
        makefile_rules = get_makefile_rules()

    return [ExtendTool, ExtendService]
