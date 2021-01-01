from leap_mn.makefile import MakefileRule
from moonleap import Resource, chop0

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
render_function_by_resource_type = []
