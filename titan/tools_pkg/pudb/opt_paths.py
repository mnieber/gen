import ramda as R
from moonleap import get_session
from titan.tools_pkg.optdir import OptPath


def pudb_opt_path():
    return OptPath(
        is_dir=True,
        from_path=R.path_or("pudb", ["pudb_opt_path"])(get_session().get_tweaks()),
        to_path="/root/.config/pudb",
    )


def ipython_opt_path():
    return OptPath(
        is_dir=True,
        from_path="ipython",
        to_path="/root/.ipython",
    )
