import moonleap.resource.props as P
from moonleap import RenderTemplates, extend, tags
from moonleap.verbs import has
from titan.project_pkg.service import Service

from .resources import Vandelay


@tags(["vandelay"])
def create_vandelay(term, block):
    vandelay = Vandelay(type=term.data, name="vandelay")
    vandelay.output_path = "../.vandelay"
    return vandelay


def get_template_filename(vandelay):
    return f"templates/vandelay-{vandelay.type}.js.j2"


@extend(Vandelay)
class ExtendVandelay(RenderTemplates(__file__, get_template_filename)):
    service = P.parent(Service, has)
