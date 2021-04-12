import moonleap.resource.props as P
from moonleap import extend, rule
from moonleap.verbs import has
from moonleap_project.project import Project
from moonleap_project.service import Service


@rule("project", has, "service")
def project_has_service(project, service):
    service.output_paths.add_source(project)


@extend(Project)
class ExtendProject:
    services = P.child(has, "service")


@extend(Service)
class ExtendService:
    project = P.parent(Project, has, "service")
