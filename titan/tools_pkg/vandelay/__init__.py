from pathlib import Path

import ramda as R
from moonleap import RenderTemplates, add, create, extend, get_session
from titan.project_pkg.vscodeproject.resources import VsCodeProjectConfig

from .resources import Vandelay


def _vandelay_path():
    settings = get_session().settings
    default_base_dir = R.path_or("", ["references", "src"])(settings)
    return str(Path(default_base_dir) / ".vandelay")


@create(["vandelay"])
def create_vandelay(term, block):
    vandelay = Vandelay(type=term.data, name="vandelay")
    vandelay.output_path = "../.vandelay"
    add(vandelay, VsCodeProjectConfig(paths=[_vandelay_path()]))
    return vandelay


def get_template_filename(vandelay):
    return f"templates/vandelay-{vandelay.type}.js.j2"


@extend(Vandelay)
class ExtendVandelay(RenderTemplates(__file__, get_template_filename)):
    pass
