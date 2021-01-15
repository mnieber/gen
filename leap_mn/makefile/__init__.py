from pathlib import Path

import moonleap.props as P
from leap_mn.layer import LayerConfig
from leap_mn.pkgdependency import PkgDependency
from leap_mn.service import Service
from leap_mn.tool import Tool
from moonleap import MemFun, extend, rule, tags
from moonleap.render_resources import load_template

from . import layer_configs as LC
from .resources import Makefile, MakefileRule


@tags(["makefile"])
def create_makefile(term, block):
    makefile = Makefile()
    makefile.pkg_dependencies.add(PkgDependency(["make"], is_dev=True))
    makefile.layer_configs.add(LayerConfig(LC.get_make_options()))
    return makefile


@rule("makefile", "running", "*", fltr_obj=P.fltr_instance(Tool))
def makefile_running_tool(makefile, tool):
    makefile.service.add_to_tools(tool)


def _render(self, template_renderer):
    output_sub_dir = self.output_paths.merged.location
    templates_path = Path(__file__).parent / "templates"
    for template_fn in templates_path.glob("*"):
        template_renderer.render(output_sub_dir, self, template_fn)


@extend(Makefile)
class ExtendMakefile:
    render = MemFun(_render)
    rules = P.children("has", "makefile_rule")
    service = P.parent(Service, "has", "makefile")
