from pathlib import Path

import moonleap.extension.props as P
from moonleap import (
    MemFun,
    RootResource,
    create,
    extend,
    get_root_resource,
    kebab_to_camel,
    rule,
)
from moonleap.extension.memfield import MemField
from moonleap.spec.verbs import has

from . import props
from .resources import Project


@create("project")
def create_project(term):
    return Project(name=kebab_to_camel(term.data), kebab_name=term.data)


@rule("project")
def root_resource_renders_project(project):
    get_root_resource().project = project


@extend(Project)
class ExtendProject:
    services = P.children(
        has, "service", lambda services: sorted(services, key=lambda x: x.name)
    )
    get_service_by_name = MemFun(props.get_service_by_name)


@extend(RootResource)
class ExtendRootResource:
    project = MemField(lambda: None)
