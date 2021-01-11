from leap_mn.makefile import MakefileRule
from leap_mn.pipdependency import PipDependencyDev
from moonleap import Resource, chop0, tags

makefile_rule = chop0(
    """
pip-compile:
    pip-compile requirements.in -o requirements.txt
    pip-compile requirements.dev.in -o requirements.dev.txt
"""
)


class PipCompile(Resource):
    def __init__(self):
        super().__init__()


@tags(["pip-compile"])
def create_pip_compile(term, block):
    pip_compile = PipCompile()
    pip_compile.add_child(MakefileRule(makefile_rule))
    pip_compile.add_child(PipDependencyDev(["pip-tools"]))
    return pip_compile


meta = {}
