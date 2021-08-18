import moonleap.resource.props as P
from moonleap import Prop, RenderTemplates, add, extend, register_add, tags
from moonleap.verbs import has
from titan.project_pkg.service import Service, Tool
from titan.tools_pkg.pkgdependency import PkgDependency

from . import layer_configs, props
from .resources import Makefile, MakefileRule  # noqa


@register_add(MakefileRule)
def add_makefile_rule(resource, makefile_rule):
    resource.makefile_rules.add(makefile_rule)


class StoreMakefileRules:
    makefile_rules = P.tree(has, "makefile")


@tags(["makefile"])
def create_makefile(term, block):
    makefile = Makefile(name="makefile")

    add(makefile, PkgDependency(["make"], is_dev=True))
    add(makefile, layer_configs.get())

    return makefile


@extend(Makefile)
class ExtendMakefile(StoreMakefileRules, RenderTemplates(__file__)):
    service = P.parent(Service, has)


@extend(Service)
class ExtendService:
    makefile_rules = Prop(props.get_makefile_rules())


@extend(Tool)
class ExtendTool(StoreMakefileRules):
    pass
