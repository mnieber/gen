from pathlib import Path

import moonleap.resource.props as P
from moonleap import Prop, add, create, extend, register_add, rule
from moonleap.verbs import has
from titan.project_pkg.service import Service, Tool
from titan.tools_pkg.pkgdependency import PkgDependency

from . import dodo_layer_configs, props
from .resources import Makefile, MakefileRule  # noqa


@register_add(MakefileRule)
def add_makefile_rule(resource, makefile_rule):
    resource.makefile_rules.add(makefile_rule)


class StoreMakefileRules:
    makefile_rules = P.tree("makefile_rules")


base_tags = [("makefile", ["tool"])]


@create("makefile")
def create_makefile(term):
    makefile = Makefile(name="makefile")
    makefile.add_template_dir(Path(__file__).parent / "templates")

    add(makefile, PkgDependency(["make"], target="prod"))
    add(makefile, dodo_layer_configs.get())

    return makefile


@rule("service", has, "makefile")
def service_has_makefile(service, makefile):
    service.project.add_template_dir(Path(__file__).parent / "templates_project")


@extend(Makefile)
class ExtendMakefile(StoreMakefileRules):
    pass


@extend(Service)
class ExtendService:
    makefile_rules = Prop(props.get_makefile_rules())


@extend(Tool)
class ExtendTool(StoreMakefileRules):
    pass
