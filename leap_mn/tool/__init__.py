import moonleap.props as props
from moonleap.config import extend, rule

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
        makefile_rules_dev = props.children("has", "dev:makefile-rule")
        layer_config = props.child("has", "layer-config")

    @extend(Service)
    class ExtendService:
        tools = props.children("has", "tool")

    return [ExtendTool, ExtendService]
