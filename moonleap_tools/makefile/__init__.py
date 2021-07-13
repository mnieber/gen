import moonleap.resource.props as P
from moonleap import MemFun, add, extend, register_add, render_templates, tags
from moonleap.verbs import has, runs
from moonleap_tools.pkgdependency import PkgDependency
from moonleap_tools.tool import Tool

from . import layer_configs
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


def meta():
    from moonleap_project.service import Service

    @extend(Makefile)
    class ExtendMakefile(StoreMakefileRules):
        render = MemFun(render_templates(__file__))
        service = P.parent(Service, has)

    return [ExtendMakefile]
