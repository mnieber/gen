from utils import chop0

makefile_rule = chop0(
    """
pip-compile:
    pip-compile requirements.in -o requirements.txt",
    pip-compile requirements.dev.in -o requirements.dev.txt",
"""
)


def update(self, resource, term, line, block):
    makefile_res = block.get_resource_by_tag("makefile")
    if makefile_res:
        makefile_res.add_rule(makefile_rule)
