import moonleap.props as P
from leap_mn.layer import StoreLayerConfigs
from leap_mn.outputpath import StoreOutputPaths
from moonleap import extend, rule, tags

from .resources import Project


@rule("project", "has", "service")
def project_has_service(project, service):
    service.output_paths.add_source(project)


@tags(["project"])
def create_project(term, block):
    project = Project(term.data)
    project.set_output_path("src/")
    return project


@extend(Project)
class ExtendProject(StoreLayerConfigs, StoreOutputPaths):
    services = P.child("has", "service")
    src_dir = P.child("has", "src-dir")
