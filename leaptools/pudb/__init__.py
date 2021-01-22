import moonleap.resource.props as P
from leapproject.service import Service
from leaptools.pipdependency import PipRequirement
from moonleap import add, extend, rule, tags
from moonleap.verbs import has, with_

from . import opt_paths
from .resources import Pudb


@tags(["pudb"])
def create_pudb(term, block):
    pudb = Pudb()

    add(pudb, PipRequirement(["pudb"]))
    add(pudb, opt_paths.pudb_opt_path)
    add(pudb, opt_paths.ipython_opt_path)

    return pudb


@rule("service", has, "pudb")
def service_has_pudb(service, pudb):
    service.add_tool(pudb)
