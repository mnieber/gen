from dataclasses import dataclass
from pathlib import Path

import moonleap.resource.props as P
from moonleap import create, create_forward, empty_rule, extend, rule
from moonleap.verbs import has
from titan.project_pkg.service import Service, Tool

rules = [
    (("service", has, "makefile"), empty_rule()),
]

base_tags = [
    ("makefile", ["tool"]),
]


@dataclass
class Makefile(Tool):
    pass


@create("makefile")
def create_makefile(term):
    makefile = Makefile("makefile")
    makefile.template_dir = Path(__file__).parent / "templates"
    makefile.template_context = dict(makefile=makefile)
    return makefile


@create("project:makefile")
def create_project_makefile(term):
    makefile = Makefile("project-makefile")
    return makefile


@rule("project")
def project_created(project):
    return create_forward(project, has, "project:makefile")


@rule("project", has, "project:makefile")
def project_has_project_makefile(project, makefile):
    project.renders(
        [makefile],
        ".",
        dict(makefile=makefile),
        [Path(__file__).parent / "templates_project"],
    )


@rule("service")
def service_created(service):
    return create_forward(service, has, ":makefile")


@extend(Service)
class ExtendService:
    makefile = P.child(has, "makefile")
