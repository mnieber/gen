from pathlib import Path

import ramda as R
from moonleap import add, create, get_session
from titan.project_pkg.vscodeproject.resources import VsCodeProjectConfig

from .resources import Vandelay

base_tags = [("vandelay", ["tool"])]


def _vandelay_path():
    settings = get_session().settings
    default_base_dir = R.path_or("", ["references", "src"])(settings)
    return str(Path(default_base_dir) / ".vandelay")


@create("vandelay")
def create_vandelay(term):
    vandelay = Vandelay(type=term.data, name="vandelay")
    vandelay.output_path = "../.vandelay"
    vandelay.add_template_dir(get_template_filename),
    add(vandelay, VsCodeProjectConfig(paths=[_vandelay_path()]))
    return vandelay


def get_template_filename(vandelay):
    return Path(__file__).parent / f"templates/vandelay-{vandelay.type}.js.j2"
