from moonleap import Resource


class GitRepository(Resource):
    def __init__(self, url):
        self.url = url

    def describe(self):
        return dict(url=self.url)


def create(term, block):
    return [GitRepository(term.data)]


tags = ["git-repository"]
render_function_by_resource_type = []
