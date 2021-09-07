from dataclasses import dataclass
from pathlib import Path

from moonleap import add, create, extend, rule
from moonleap.verbs import has
from titan.project_pkg.service import Tool
from titan.tools_pkg.pipdependency import PipDependency

from . import dodo_layer_configs, makefile_rules


@dataclass
class PipCompile(Tool):
    pass


@rule("service", has, "pip-compile")
def service_has_pip_compile(service, pip_compile):
    service.add_template_dir(Path(__file__).parent / "templates_service")


@create("pip-compile", ["tool"])
def create_pip_compile(term, block):
    pip_compile = PipCompile(name="pip-compile")

    add(pip_compile, makefile_rules.get_pipcompile())
    add(pip_compile, makefile_rules.get_install())
    add(pip_compile, dodo_layer_configs.get())
    add(pip_compile, PipDependency(["pip-tools"], is_dev=True))

    return pip_compile


@extend(PipCompile)
class ExtendPipCompile:
    pass
