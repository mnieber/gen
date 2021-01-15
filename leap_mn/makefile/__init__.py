import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.pkgdependency import PkgDependency
from leap_mn.service import Service
from leap_mn.tool import Tool
from moonleap import extend, render_templates, rule, tags

from . import layer_configs as LC
from .resources import Makefile, MakefileRule  # noqa


@tags(["makefile"])
def create_makefile(term, block):
    makefile = Makefile()
    makefile.pkg_dependencies.add(PkgDependency(["make"], is_dev=True))
    makefile.layer_configs.add(LayerConfig(LC.get_make_options()))
    return makefile


@rule("makefile", "running", "*", fltr_obj=P.fltr_instance(Tool))
def makefile_running_tool(makefile, tool):
    makefile.service.add_to_tools(tool)


@extend(Makefile)
class ExtendMakefile:
    render = render_templates(__file__)
    rules = P.children("has", "makefile_rule")
    service = P.parent(Service, "has", "makefile")
