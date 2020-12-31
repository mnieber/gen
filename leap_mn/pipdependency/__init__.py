from leap_mn import gitrepository
from moonleap.resource import Resource


class PipDependency(Resource):
    def __init__(self, package_name):
        self.package_name = package_name

    def describe(self):
        return {str(self): dict(package_name=self.package_name)}


def create(term, line, block):
    return [PipDependency(term.data)]


tags = ["pip-dependency"]
