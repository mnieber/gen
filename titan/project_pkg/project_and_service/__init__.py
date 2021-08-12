import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from titan.project_pkg.project import Project
from titan.project_pkg.service import Service


@rule("project", has, "service")
def project_has_service(project, service):
    service.output_paths.add_source(project)


@extend(Project)
class ExtendProject:
    services = P.children(has, "service")


@extend(Service)
class ExtendService:
    project = P.parent(Project, has)
