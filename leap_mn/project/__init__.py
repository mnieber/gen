from leap_mn.service import Service
from leap_mn.srcdir import SrcDir
from moonleap import Resource, tags


class Project(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["project"], is_ittable=True)
def create(term, block):
    return [Project(term.data)]


meta = {Project: dict(children={"services": [Service], "src_dir": SrcDir})}
