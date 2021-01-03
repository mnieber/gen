from moonleap import Resource, reduce


class SrcDir(Resource):
    def __init__(self, location):
        self.location = location or "src"
        self.git_repo = None

    def describe(self):
        return dict(
            location=self.location,
            git_repo=self.git_repo.describe() if self.git_repo else None,
        )


def create(term, block):
    return [SrcDir(term.data)]


@reduce(a_resource=SrcDir, b_resource="leap_mn.GitRepository")
def set_git_repo(src_dir, git_repo):
    if src_dir.is_mentioned_in_same_line(git_repo, is_ordered=False):
        src_dir.git_repo = git_repo


tags = ["src-dir"]
