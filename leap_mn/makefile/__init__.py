from dataclasses import dataclass

import moonleap.props as props
from leap_mn.layerconfig import LayerConfig
from leap_mn.pkgdependency import PkgDependency
from leap_mn.tool import Tool
from moonleap import Resource, output_dir_from, rule, tags
from moonleap.config import config, extend


@dataclass
class Makefile(Tool):
    pass


@dataclass
class MakefileRule(Resource):
    text: str


def get_layer_config():
    return dict(ROOT=dict(decorators=dict(docker=["make"])))


@tags(["makefile"])
def create_makefile(term, block):
    makefile = Makefile()
    makefile.add_to_pkg_dependencies_dev(PkgDependency(["make"]))
    makefile.layer_config = LayerConfig(get_layer_config())
    return makefile


@rule("makefile", "running", "*")
def makefile_running_pip_compile(makefile, tool, fltr_obj=props.fltr_instance(Tool)):
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
