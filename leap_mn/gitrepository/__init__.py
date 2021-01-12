from moonleap import tags

from .resources import GitRepository


@tags(["git-repository"])
def create_git_repository(term, block):
    return GitRepository(url=term.data)


def meta():
    return []
