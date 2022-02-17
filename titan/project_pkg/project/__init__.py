import moonleap.resource.props as P
from moonleap import StoreOutputPaths, create, empty_rule, extend, kebab_to_camel
from moonleap.render.storetemplatedirs import StoreTemplateDirs
from moonleap.verbs import has

from .resources import Project


@create("project")
def create_project(term):
    project = Project(name=kebab_to_camel(term.data))
    project.output_path = "src/"
    return project


rules = [(("project", has, "src-dir"), empty_rule())]


@extend(Project)
class ExtendProject(StoreOutputPaths, StoreTemplateDirs):
    src_dir = P.child(has, "src-dir")
