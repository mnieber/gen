from leap_mn.pipdependency import PipDependency
from moonleap import Resource


class PytestHtml(Resource):
    def __init__(self):
        super().__init__()


def create(term, block):
    return [PytestHtml(), PipDependency("pytest-html")]


tags = ["pytest-html"]
