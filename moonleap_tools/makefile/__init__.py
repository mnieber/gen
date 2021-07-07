import moonleap.resource.props as P
from moonleap import (
    MemFun,
    add,
    create_forward,
    extend,
    register_add,
    render_templates,
    rule,
    tags,
)
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


@rule("makefile", runs, "*", fltr_obj=P.fltr_instance(Tool))
def makefile_running_tool(makefile, tool):
    return create_forward(makefile.service, has, ":tool", tool)


def meta():
    from moonleap_project.service import Service

    @extend(Makefile)
    class ExtendMakefile(StoreMakefileRules):
        render = MemFun(render_templates(__file__))
        service = P.parent(Service, has)

    return [ExtendMakefile]
