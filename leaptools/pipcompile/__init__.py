from dataclasses import dataclass

from leaptools.makefile import MakefileRule
from leaptools.pipdependency import PipDependency
from leaptools.tool import Tool
from moonleap import chop0, extend, render_templates, rule, tags

has = ("has", "uses")

makefile_rule = chop0(
    """
pip-compile:
    pip-compile requirements.in -o requirements.txt
    pip-compile requirements.dev.in -o requirements.dev.txt
"""
)


@dataclass
class PipCompile(Tool):
    pass


@rule("service", has, "pip-compile")
def service_has_pip_compile(service, pip_compile):
    service.add_tool(pip_compile)


@tags(["pip-compile"])
def create_pip_compile(term, block):
    pip_compile = PipCompile()
    pip_compile.add_to_makefile_rules(MakefileRule(makefile_rule))
    pip_compile.pip_dependencies.add(PipDependency(["pip-tools"], is_dev=True))
    return pip_compile


@extend(PipCompile)
class ExtendPipCompile:
    render = render_templates(__file__)
