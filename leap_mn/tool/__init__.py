import moonleap.props as props
import ramda as R
from moonleap.config import extend, rule

from .localprops import get_makefile_rules, get_package_names
from .resources import Tool


@rule("service", "has", "*", fltr_obj=props.fltr_instance(Tool))
def service_has_tool(service, tool):
    service.add_to_tools(tool)


def meta():
    from leap_mn.service import Service

    @extend(Tool)
    class ExtendTool:
        pip_dependencies = props.children("has", ":pip-dependency")
        pip_dependencies_dev = props.children("has", "dev:pip-dependency")
        pkg_dependencies = props.children("has", ":pkg-dependency")
        pkg_dependencies_dev = props.children("has", "dev:pkg-dependency")
        makefile_rules = props.children("has", ":makefile-rule")
        layer_config = props.child("has", "layer-config")

    @extend(Service)
    class ExtendService:
        tools = props.children("has", "tool")
        pip_dependencies = get_package_names("pip_dependencies")
        pip_dependencies_dev = get_package_names("pip_dependencies_dev")
        pkg_dependencies = get_package_names("pkg_dependencies")
        pkg_dependencies_dev = get_package_names("pkg_dependencies_dev")
        makefile_rules = get_makefile_rules()

    return [ExtendTool, ExtendService]
