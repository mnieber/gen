import moonleap.resource.props as P
from moonleap import extend, feeds
from moonleap.verbs import has
from titan.project_pkg.project import Project
from titan.project_pkg.service import Service

rules = [(("project", has, "service"), feeds("output_paths"))]


@extend(Project)
class ExtendProject:
    services = P.children(has, "service")


@extend(Service)
class ExtendService:
    project = P.parent("project", has, required=True)
