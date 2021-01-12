import moonleap.props as props
from leap_mn.layerconfig import LayerConfig
from leap_mn.pkgdependency import PkgDependency
from leap_mn.tool import Tool
from moonleap import extend, output_dir_from, rule, tags

from .layer_configs import get_layer_config
from .resources import Makefile, MakefileRule


@tags(["makefile"])
def create_makefile(term, block):
    makefile = Makefile()
    makefile.add_to_pkg_dependencies_dev(PkgDependency(["make"]))
    makefile.layer_config = LayerConfig(get_layer_config())
    return makefile


@rule("makefile", "running", "*", fltr_obj=props.fltr_instance(Tool))
def makefile_running_tool(makefile, tool):
    makefile.service.add_to_tools(tool)


def meta():
    from leap_mn.service import Service

    @extend(Makefile)
    class ExtendMakefile:
        templates = "templates"
        output_dir = output_dir_from("service")
        rules = props.children("has", "makefile_rule")
        service = props.parent(Service, "has", "makefile")

    return [ExtendMakefile]
