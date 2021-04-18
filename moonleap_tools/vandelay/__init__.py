import moonleap.resource.props as P
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import Service, service_has_tool_rel
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import Vandelay


@tags(["vandelay"])
def create_vandelay(term, block):
    vandelay = Vandelay(type=term.data)
    vandelay.output_path = ".vandelay"
    return vandelay


@rule("service", has, "vandelay")
def service_has_vandelay(service, vandelay):
    return service_has_tool_rel(service, vandelay)


def get_template_filename(vandelay):
    return f"templates/vandelay-{vandelay.type}.js.j2"


@extend(Vandelay)
class ExtendVandelay:
    service = P.parent(Service, has, "vandelay")
    render = MemFun(render_templates(__file__, get_template_filename))
