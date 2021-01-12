from dataclasses import dataclass

import moonleap.props as props
from moonleap import Resource, tags
from moonleap.config import extend


@dataclass
class SrcDir(Resource):
    location: str


@tags(["src-dir"])
def create_src_dir(term, block):
    return SrcDir(location=term.data or "src")


def meta():
    @extend(SrcDir)
    class ExtendSrcDir:
        git_repo = props.child("has", "git-repository")

    return [ExtendSrcDir]
