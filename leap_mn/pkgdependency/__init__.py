import ramda as R
from moonleap import Resource, tags
from moonleap.props import Prop


class PkgDependency(Resource):
    def __init__(self, package_names):
        super().__init__()
        self.package_names = package_names


class PkgDependencyDev(PkgDependency):
    pass


def list_of_packages(resource_type):
    def prop(self):
        items = self.children_of_type(resource_type)
        return R.pipe(
            R.map(R.prop("package_names")),
            R.chain(R.identity),
            sorted,
        )(items)

        # return sorted(R.chain(R.identity, [x.package_names for x in items]))

    return Prop(prop, child_resource_type=resource_type)


@tags(["pkg-dependency"])
def create(term, block):
    return [PkgDependency([term.data])]


@tags(["pkg-dependency-dev"])
def create(term, block):
    return [PkgDependencyDev([term.data])]


meta = {}
