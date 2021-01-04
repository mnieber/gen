from moonleap import Resource


class GitRepository(Resource):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def describe(self):
        return dict(url=self.url)


def create(term, block):
    return [GitRepository(term.data)]


tags = ["git-repository"]
