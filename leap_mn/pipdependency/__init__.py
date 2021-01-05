from moonleap import Resource, tags


class PipDependency(Resource):
    def __init__(self, package_name):
        super().__init__()
        self.package_name = package_name


class PipDependencyDev(PipDependency):
    pass


@tags(["pip-dependency"])
def create(term, block):
    return [PipDependency(term.data)]


@tags(["pip-dependency-dev"])
def create(term, block):
    return [PipDependencyDev(term.data)]


meta = {}
