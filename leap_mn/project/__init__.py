import moonleap.props as P
from leap_mn.layer import StoreLayerConfigs
from moonleap import extend, tags

from .resources import Project


@tags(["project"])
def create_project(term, block):
    return Project(term.data)


@extend(Project)
class ExtendProject(StoreLayerConfigs):
    output_dir = "src"
    services = P.child("has", "service")
    src_dir = P.child("has", "src-dir")
