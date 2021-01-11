from dataclasses import dataclass

from moonleap import Resource, tags


@dataclass
class GitRepository(Resource):
    url: str


@tags(["git-repository"])
def create_git_repository(term, block):
    return GitRepository(url=term.data)


def meta():
    return []
