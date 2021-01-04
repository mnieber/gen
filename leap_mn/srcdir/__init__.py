from leap_mn.gitrepository import GitRepository
from moonleap import Resource, tags


class SrcDir(Resource):
    def __init__(self, location):
        super().__init__()
        self.location = location or "src"


@tags(["src-dir"])
def create(term, block):
    return [SrcDir(term.data)]


meta = {SrcDir: dict(children={"git_repo": GitRepository})}
