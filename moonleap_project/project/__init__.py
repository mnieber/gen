import moonleap.resource.props as P
from moonleap import StoreOutputPaths, extend, kebab_to_camel, tags
from moonleap.verbs import has

from .resources import Project


@tags(["project"])
def create_project(term, block):
    project = Project(kebab_to_camel(term.data))
    project.output_path = "src/"
    return project


@extend(Project)
class ExtendProject(StoreOutputPaths):
    src_dir = P.child(has, "src-dir")
