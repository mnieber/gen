import moonleap.resource.props as P
from leapdodo.layer import LayerConfig
from leapproject.service import Service
from leaptools.pkgdependency import PkgDependency
from leaptools.tool import Tool, service_has_tool
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
    if tool not in makefile.service.tools:
        service_has_tool(makefile.service, tool)


@extend(Makefile)
class ExtendMakefile:
    render = render_templates(__file__)
    rules = P.children("has", "makefile_rule")
    service = P.parent(Service, "has", "makefile")
