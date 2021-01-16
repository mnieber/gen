import moonleap.resource.props as P
from leapdodo.layer import StoreLayerConfigs
from moonleap import StoreOutputPaths, extend, rule, tags

from .resources import Project


@rule("project", "has", "service")
def project_has_service(project, service):
    service.output_paths.add_source(project)


@tags(["project"])
def create_project(term, block):
    project = Project(term.data)
    project.output_path = "src/"
    return project


@extend(Project)
class ExtendProject(StoreLayerConfigs, StoreOutputPaths):
    services = P.child("has", "service")
    src_dir = P.child("has", "src-dir")
