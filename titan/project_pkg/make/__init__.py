from dataclasses import dataclass

import moonleap.packages.extensions.props as P
from moonleap import create, create_forward, empty_rule, extend, rule
from moonleap.blocks.verbs import has
from titan.project_pkg.service import Service, Tool

base_tags = {
    "makefile": ["tool"],
}


@dataclass
class Makefile(Tool):
    pass


@create("makefile")
def create_makefile(term):
    makefile = Makefile("makefile")
    return makefile


@create("project:makefile")
def create_project_makefile(term):
    makefile = Makefile("project-makefile")
    return makefile


@rule("project")
def created_project(project):
    return create_forward(project, has, "project:makefile")


@rule("service")
def created_service(service):
    return create_forward(service, has, ":makefile")


@extend(Service)
class ExtendService:
    makefile = P.child(has, "makefile")


rules = {
    "service": {(has, "makefile"): empty_rule()},
    "project": {(has, "project:makefile"): empty_rule()},
}
