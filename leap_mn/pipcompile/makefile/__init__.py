from moonleap.parser.block import has_terms_in_same_line
from moonleap.utils import chop0

makefile_rule = chop0(
    """
pip-compile:
    pip-compile requirements.in -o requirements.txt",
    pip-compile requirements.dev.in -o requirements.dev.txt",
"""
)


def update(block, pipcompile_term, makefile_term):
    if has_terms_in_same_line(block, makefile_term, pipcompile_term):
        block.get_resource(makefile_term).add_rule(makefile_rule)
