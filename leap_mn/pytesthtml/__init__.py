from leap_mn.pipdependency import PipDependency
from moonleap import Resource, tags


class PytestHtml(Resource):
    def __init__(self):
        super().__init__()


@tags(["pytest-html"])
def create(term, block):
    return [PytestHtml(), PipDependency(["pytest-html"])]


meta = {}
