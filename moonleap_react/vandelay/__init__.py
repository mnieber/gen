from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import service_has_tool_rel
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import Vandelay


@tags(["vandelay"])
def create_vandelay(term, block):
    vandelay = Vandelay(type=term.data)
    return vandelay


@rule("service", has, "vandelay")
def service_has_vandelay(service, vandelay):
    vandelay.output_paths.add_source(service)
    return service_has_tool_rel(service, vandelay)


@extend(Vandelay)
class ExtendVandelay:
    render = MemFun(props.render)
