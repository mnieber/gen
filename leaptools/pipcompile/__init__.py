from dataclasses import dataclass

from leaptools.pipdependency import PipDependency
from leaptools.tool import Tool
from moonleap import add, extend, render_templates, rule, tags
from moonleap.verbs import has

from . import layer_configs, makefile_rules


@dataclass
class PipCompile(Tool):
    pass


@rule("service", has, "pip-compile")
def service_has_pip_compile(service, pip_compile):
    service.add_tool(pip_compile)


@tags(["pip-compile"])
def create_pip_compile(term, block):
    pip_compile = PipCompile()

    add(pip_compile, makefile_rules.get())
    add(pip_compile, layer_configs.get())
    add(pip_compile, PipDependency(["pip-tools"], is_dev=True))

    return pip_compile


@extend(PipCompile)
class ExtendPipCompile:
    render = render_templates(__file__)
