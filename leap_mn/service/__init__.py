from leap_mn.pipdependency import PipDependency, PipDependencyDev
from leap_mn.pkgdependency import PkgDependency, PkgDependencyDev
from leap_mn.srcdir import SrcDir
from moonleap import Resource, output_path_from, tags


class Service(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name


@tags(["service"], is_ittable=True)
def create(term, block):
    return [Service(term.data)]


meta = {
    Service: dict(
        output_dir=lambda x: str(output_path_from("project")(x) / x.name),
        children={
            "pip_dependencies": [PipDependency],
            "pip_dependencies_dev": [PipDependencyDev],
            "pkg_dependencies": [PkgDependency],
            "pkg_dependencies_dev": [PkgDependencyDev],
            "src_dir": SrcDir,
        },
        parents={"project": "leap_mn.project.Project"},
    )
}
