from leap_mn.service import Service
from moonleap import Resource, tags


class Dockerfile(Resource):
    def __init__(self, is_dev):
        super().__init__()
        self.pip_package_names = []
        self.package_names = []

    def add_pip_package(self, package_name):
        if package_name not in self.pip_package_names:
            self.pip_package_names.append(package_name)

    def add_package(self, package_name):
        if package_name not in self.package_names:
            self.package_names.append(package_name)


@tags(["docker-file"])
def create(term, block):
    return [Dockerfile()]


@tags(["docker-file-dev"])
def create(term, block):
    return [DockerfileDev()]


class DockerfileDev(Dockerfile):
    pass


meta = {
    Dockerfile: {"templates": "templates"},
    DockerfileDev: {"templates": "templates-dev"},
}
