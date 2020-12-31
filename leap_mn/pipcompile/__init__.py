from leap_mn.makefilerule import MakefileRule
from moonleap.resource import Resource
from moonleap.utils import chop0

makefile_rule = chop0(
    """
pip-compile:
    pip-compile requirements.in -o requirements.txt",
    pip-compile requirements.dev.in -o requirements.dev.txt",
"""
)


class PipCompile(Resource):
    def __init__(self):
        pass


def create(term, block):
    return [PipCompile(), MakefileRule(makefile_rule)]


tags = ["pip-compile"]
