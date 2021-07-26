import moonleap.resource.props as P
from moonleap import MemFun, extend, render_templates, tags
from moonleap.verbs import has
from moonleap_project.service import Service

from .resources import Vandelay


@tags(["vandelay"])
def create_vandelay(term, block):
    vandelay = Vandelay(type=term.data, name="vandelay")
    vandelay.output_path = ".vandelay"
    return vandelay


def get_template_filename(vandelay):
    return f"templates/vandelay-{vandelay.type}.js.j2"


@extend(Vandelay)
class ExtendVandelay:
    service = P.parent(Service, has)
    render = MemFun(render_templates(__file__, get_template_filename))
