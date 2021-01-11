import moonleap.props as props
from leap_mn.layerconfig import LayerConfig
from leap_mn.pipdependency import PipDependency, PipDependencyDev
from leap_mn.pkgdependency import PkgDependency, PkgDependencyDev, list_of_packages
from leap_mn.srcdir import SrcDir
from moonleap import Resource, output_path_from, tags


class Service(Resource):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"Service name={self.name}"


def get_layer_config():
    return dict(install_dir="/app", src_dir="${/SERVER/install_dir}/src")


@tags(["service"])
def create_service(term, block):
    service = Service(term.data)
    service.add_child(LayerConfig(dict(SERVER=get_layer_config())))
    return service


def meta():
    from leap_mn.project import Project

    return {
        Service: dict(
            output_dir=lambda x: str(output_path_from("project")(x) / x.name),
            props={
                "pip_dependencies": list_of_packages(PipDependency),
                "pip_dependencies_dev": list_of_packages(PipDependencyDev),
                "pkg_dependencies": list_of_packages(PkgDependency),
                "pkg_dependencies_dev": list_of_packages(PkgDependencyDev),
                "src_dir": props.child_of_type(SrcDir),
                "project": props.parent_of_type(Project),
                "layer_config": props.child_of_type(LayerConfig),
            },
        )
    }
