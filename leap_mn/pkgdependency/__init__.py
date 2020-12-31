from leap_mn import gitrepository
from moonleap.config import reduce
from moonleap.resource import Resource


class PkgDependency(Resource):
    def __init__(self, package_name, is_dev):
        self.package_name = package_name
        self.is_dev = is_dev

    def describe(self):
        return dict(package_name=self.package_name, is_dev=self.is_dev)


def create(term, block):
    return [PkgDependency(term.data, is_dev=term.tag == "pkg-dependency-dev")]


tags = ["pkg-dependency", "pkg-dependency-dev"]
