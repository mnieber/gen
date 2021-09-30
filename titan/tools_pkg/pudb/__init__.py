from moonleap import add, create
from titan.tools_pkg.pipdependency import PipRequirement

from . import opt_paths
from .resources import Pudb

base_tags = [("pudb", ["tool"])]


@create("pudb")
def create_pudb(term, block):
    pudb = Pudb(name="pudb")

    add(pudb, PipRequirement(["pudb", "ipython"], is_dev=True))
    add(pudb, opt_paths.pudb_opt_path())
    add(pudb, opt_paths.ipython_opt_path())

    return pudb
