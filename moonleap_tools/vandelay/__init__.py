import moonleap.resource.props as P
from moonleap import MemFun, add, extend, render_templates, rule, tags
from moonleap.verbs import has
from moonleap_project.service import Service
from moonleap_react.nodepackage import load_node_package_config

from . import props
from .resources import Vandelay


@tags(["vandelay"])
def create_vandelay(term, block):
    vandelay = Vandelay(type=term.data)
    vandelay.output_path = ".vandelay"
    return vandelay


def get_template_filename(vandelay):
    return f"templates/vandelay-{vandelay.type}.js.j2"


@extend(Vandelay)
class ExtendVandelay:
    service = P.parent(Service, has, "vandelay")
    render = MemFun(render_templates(__file__, get_template_filename))
