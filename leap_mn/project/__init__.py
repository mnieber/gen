import moonleap.props as props
from moonleap import tags
from moonleap.config import extend

from .resources import Project


@tags(["project"])
def create_project(term, block):
    return Project(term.data)


def meta():
    @extend(Project)
    class ExtendProject:
        output_dir = "src"
        services = props.child("has", "service")
        src_dir = props.child("has", "src-dir")

    return [ExtendProject]
