import moonleap.props as props
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
        props={
            "pip_dependencies": props.children_of_type(PipDependency),
            "pip_dependencies_dev": props.children_of_type(PipDependencyDev),
            "pkg_dependencies": props.children_of_type(PkgDependency),
            "pkg_dependencies_dev": props.children_of_type(PkgDependencyDev),
            "src_dir": props.child_of_type(SrcDir),
            "project": props.parent_of_type("leap_mn.project.Project"),
        },
    )
}
