from moonleap import Resource, tags


class GitRepository(Resource):
    def __init__(self, url):
        super().__init__()
        self.url = url


@tags(["git-repository"])
def create_git_repository(term, block):
    return [GitRepository(term.data)]


meta = {}
