from moonleap import Resource, tags


class PkgDependency(Resource):
    def __init__(self, package_name, is_dev):
        super().__init__()
        self.package_name = package_name


class PkgDependencyDev(PkgDependency):
    pass


@tags(["pkg-dependency"])
def create(term, block):
    return [PkgDependency(term.data)]


@tags(["pkg-dependency-dev"])
def create(term, block):
    return [PkgDependencyDev(term.data)]
