import moonleap.resource.props as P
from moonleap import DocMeta, MemFun, Prop, extend, rule
from moonleap.verbs import has

from . import props
from .resources import Tool  # noqa


@rule("service", has, "tool")
def service_has_tool(service, tool):
    tool.output_paths.add_source(service)


def meta():
    from moonleap_project.service import Service

    @extend(Service)
    class ExtendService:
        get_pip_pkg_names = MemFun(props.get_pip_pkg_names())
        get_pip_requirements = MemFun(props.get_pip_requirements())
        get_pkg_names = MemFun(props.get_pkg_names())
        makefile_rules = Prop(props.get_makefile_rules())
        opt_dir = P.child(has, "opt-dir")
        tools = P.children(has, "tool", is_private_rel=True)

    return [ExtendService]
