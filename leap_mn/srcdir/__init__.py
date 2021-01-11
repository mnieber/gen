from dataclasses import dataclass

import moonleap.props as props
from leap_mn.gitrepository import GitRepository
from moonleap import Resource, tags
from moonleap.config import extend


@dataclass
class SrcDir(Resource):
    location: str = "src"


@tags(["src-dir"])
def create_src_dir(term, block):
    return SrcDir(term.data)


def meta():
    @extend(SrcDir)
    class ExtendSrcDir:
        git_repo = props.child("has", "git-repository")

    return [ExtendSrcDir]
