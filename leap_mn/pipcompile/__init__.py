from dataclasses import dataclass

from leap_mn.makefile import MakefileRule
from leap_mn.pipdependency import PipDependency
from leap_mn.tool import Tool
from moonleap import chop0, tags

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


@tags(["pip-compile"])
def create_pip_compile(term, block):
    pip_compile = PipCompile()
    pip_compile.add_to_makefile_rules(MakefileRule(makefile_rule))
    pip_compile.add_to_pip_dependencies(PipDependency(["pip-tools"], is_dev=True))
    return pip_compile
