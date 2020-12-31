from moonleap import Resource


class PipDependency(Resource):
    def __init__(self, package_name, is_dev=False):
        self.package_name = package_name
        self.is_dev = is_dev

    def describe(self):
        return dict(package_name=self.package_name)


def create(term, block):
    return [PipDependency(term.data)]


tags = ["pip-dependency"]
