from moonleap import Resource


class SrcDir(Resource):
    def __init__(self, location):
        super().__init__()
        self.location = location or "src"
        self.git_repo = None

    def describe(self):
        return dict(
            location=self.location,
            git_repo=self.git_repo.describe() if self.git_repo else None,
        )


def create(term, block):
    return [SrcDir(term.data)]


tags = ["src-dir"]
