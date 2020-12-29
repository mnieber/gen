from leap_mn.resource import Resource


class SrcDir(Resource):
    def __init__(self, location):
        self.location = location
        self.git_repo = None

    def describe(self):
        return {
            str(self): dict(location=self.location, git_repo=self.git_repo.describe())
        }


def create(term, line, block):
    return SrcDir(term.data)


create_rule_by_tag = {
    "src-dir": create,
}
