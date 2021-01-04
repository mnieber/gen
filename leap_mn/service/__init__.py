from leap_mn.pipdependency import PipDependency
from leap_mn.pkgdependency import PkgDependency
from leap_mn.srcdir import SrcDir
from moonleap import Resource, tags


class Service(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["service"], is_ittable=True)
def create(term, block):
    return [Service(term.data)]


meta = {
    Service: dict(
        children={
            "pip_dependencies": [PipDependency],
            "pkg_dependencies": [PkgDependency],
            "src_dir": SrcDir,
        }
    )
}
