from moonleap.resource import Resource


class GitRepository(Resource):
    def __init__(self, url):
        self.url = url

    def describe(self):
        return {str(self): dict(url=self.url)}


def create(term, line, block):
    return [GitRepository(term.data)]


tags = ["git-repository"]
