import moonleap.props as props
from leap_mn.gitrepository import GitRepository
from moonleap import Resource, tags


class SrcDir(Resource):
    def __init__(self, location):
        super().__init__()
        self.location = location or "src"


@tags(["src-dir"])
def create(term, block):
    return [SrcDir(term.data)]


meta = {SrcDir: dict(props={"git_repo": props.child_of_type(GitRepository)})}
