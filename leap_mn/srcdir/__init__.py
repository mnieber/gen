import moonleap.props as props
from moonleap import tags
from moonleap.config import extend

from .resources import SrcDir


@tags(["src-dir"])
def create_src_dir(term, block):
    return SrcDir(location=term.data or "src")


def meta():
    @extend(SrcDir)
    class ExtendSrcDir:
        git_repo = props.child("has", "git-repository")

    return [ExtendSrcDir]
