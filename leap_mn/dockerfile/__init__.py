from moonleap import Resource, reduce


class Dockerfile(Resource):
    def __init__(self, is_dev):
        self.is_dev = is_dev
        self.pip_package_names = []
        self.package_names = []

    def add_pip_package(self, package_name):
        if package_name not in self.pip_package_names:
            self.pip_package_names.append(package_name)

    def add_package(self, package_name):
        if package_name not in self.package_names:
            self.package_names.append(package_name)

    def describe(self):
        return dict(
            is_dev=self.is_dev,
            pip_install=self.pip_package_names,
            install=self.package_names,
        )


def create(term, block):
    return [Dockerfile(is_dev=term.tag == "dockerfile-dev")]


@reduce(a_resource=Dockerfile, b_resource="leap_mn.PipDependency")
def add_pip_dependency(dockerfile, pip_dependency):
    if pip_dependency.is_dev and not dockerfile.is_dev:
        return

    if pip_dependency.is_created_in_block_that_mentions(dockerfile):
        dockerfile.add_pip_package(pip_dependency.package_name)


@reduce(a_resource=Dockerfile, b_resource="leap_mn.PkgDependency")
def add_pkg_dependency(dockerfile, pkg_dependency):
    if pkg_dependency.is_dev and not dockerfile.is_dev:
        return

    if pkg_dependency.is_created_in_block_that_mentions(dockerfile):
        dockerfile.add_package(pkg_dependency.package_name)


tags = ["dockerfile", "dockerfile-dev"]
render_function_by_resource_type = []
