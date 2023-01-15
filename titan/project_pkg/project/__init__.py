from pathlib import Path

import moonleap.packages.extensions.props as P
from moonleap import MemFun, create, extend, get_root_resource, kebab_to_camel, rule
from moonleap.blocks.verbs import has

from . import props
from .resources import Project


@create("project")
def create_project(term):
    return Project(name=kebab_to_camel(term.data), kebab_name=term.data)


@rule("project")
def root_resource_renders_project(project):
    get_root_resource().renders(
        [project],
        "src",
        dict(project=project),
        [Path(__file__).parent / "templates"],
    )


@extend(Project)
class ExtendProject:
    services = P.children(
        has, "service", lambda services: sorted(services, key=lambda x: x.name)
    )
    get_service_by_name = MemFun(props.get_service_by_name)
