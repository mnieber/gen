from moonleap import Resource


class PkgDependency(Resource):
    def __init__(self, package_name, is_dev):
        super().__init__()
        self.package_name = package_name
        self.is_dev = is_dev

    def key(self):
        return self.type_id + ("-dev" if self.is_dev else "")

    def describe(self):
        return dict(package_name=self.package_name, is_dev=self.is_dev)


def create(term, block):
    return [PkgDependency(term.data, is_dev=term.tag == "pkg-dependency-dev")]


tags = ["pkg-dependency", "pkg-dependency-dev"]
