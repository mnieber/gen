import moonleap.resource.props as P
from moonleap import add_src_inv, extend
from moonleap.verbs import has
from titan.project_pkg.project import Project
from titan.project_pkg.service import Service

rules = [(("project", has, "service"), add_src_inv("output_paths"))]


@extend(Project)
class ExtendProject:
    services = P.children(has, "service")


@extend(Service)
class ExtendService:
    project = P.parent(Project, has)
