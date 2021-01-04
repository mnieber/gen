from moonleap import Resource


class PipDependency(Resource):
    def __init__(self, package_name, is_dev=False):
        super().__init__()
        self.package_name = package_name
        self.is_dev = is_dev

    def key(self):
        return self.type_id + ("-dev" if self.is_dev else "")

    def describe(self):
        return dict(package_name=self.package_name)


def create(term, block):
    return [PipDependency(term.data)]


tags = ["pip-dependency"]
