from dataclasses import dataclass

import moonleap.props as props
from moonleap import Resource, tags
from moonleap.config import extend


@dataclass
class Project(Resource):
    name: str


@tags(["project"])
def create_project(term, block):
    return Project(term.data)


def meta():
    from leap_mn.service import Service
    from leap_mn.srcdir import SrcDir

    @extend(Project)
    class ExtendProject:
        output_dir = "src"
        services = props.child("has", "service")
        src_dir = props.child("has", "src-dir")

    return [ExtendProject]
