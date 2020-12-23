from utils import chop0

from resources.resource import Resource


class PipCompile(Resource):
    def __init__(self):
        pass


class Builder:
    @staticmethod
    def create(term, line, block):
        return PipCompile()


makefile_rule = chop0(
    """
pip-compile:
    pip-compile requirements.in -o requirements.txt",
    pip-compile requirements.dev.in -o requirements.dev.txt",
"""
)
