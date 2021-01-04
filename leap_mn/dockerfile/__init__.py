from leap_mn.service import Service
from moonleap import Resource


class Dockerfile(Resource):
    def __init__(self, is_dev):
        super().__init__()
        self.is_dev = is_dev
        self.pip_package_names = []
        self.package_names = []

    @property
    def key(self):
        return self.type_id + ("-dev" if self.is_dev else "")

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


tags = ["dockerfile", "dockerfile-dev"]
