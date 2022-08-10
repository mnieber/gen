# TODO:
from moonleap import settings

# TODO:
# - add vandelay path to vscode settings


def _vandelay_path():
    settings = get_session().settings
    default_base_dir = R.path_or("", ["references", "src"])(settings)
    return str(Path(default_base_dir) / ".vandelay")
