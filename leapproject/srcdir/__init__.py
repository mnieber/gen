import moonleap.resource.props as P
from moonleap import extend, rule, tags

from .resources import SrcDir

stores = "stores"


@tags(["src-dir"])
def create_src_dir(term, block):
    return SrcDir(location=term.data or "src")


@rule("src-dir", stores, "git-repostitory")
def src_dir_stores_git_repository(src_dir, git_repository):
    src_dir.git_repo_url = git_repository.term.data
