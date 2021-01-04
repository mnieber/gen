from moonleap import Resource, tags


class SrcDir(Resource):
    def __init__(self, location):
        super().__init__()
        self.location = location or "src"
        self.git_repo = None


@tags(["src-dir"])
def create(term, block):
    return [SrcDir(term.data)]
