from leap_mn.resource import Resource


class GitRepository(Resource):
    def __init__(self, url):
        self.url = url

    def describe(self):
        return {str(self): dict(url=self.url)}


def create(term, line, block):
    return GitRepository(term.data)

    # git_dir = os.path.join(get('src_dir'), ".git")
    # if not os.path.exists(git_dir):
    #     schedule(["gh", "create", "dodo-gen"], "I will create a new project on Github")


create_rule_by_tag = {
    "git-repository": create,
}

update_rules = [
    ("leap_mn.srcdir", "srcdir"),
]
