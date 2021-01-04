from moonleap import Resource, tags


@tags(["git-repository"])
class GitRepository(Resource):
    def __init__(self, url):
        super().__init__()
        self.url = url


def create(term, block):
    return [GitRepository(term.data)]
