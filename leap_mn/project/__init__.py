import moonleap.props as P
from moonleap import tags
from moonleap.config import extend

from .resources import Project


@tags(["project"])
def create_project(term, block):
    return Project(term.data)


@extend(Project)
class ExtendProject:
    output_dir = "src"
    services = P.child("has", "service")
    src_dir = P.child("has", "src-dir")


def meta():
    return [ExtendProject]
