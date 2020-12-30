from moonleap.config import reduce
from moonleap.resource import Resource


class Dockerfile(Resource):
    def __init__(self, is_dev):
        self.is_dev = is_dev
        self.pip_package_names = []

    def describe(self):
        return {str(self): dict(is_dev=self.is_dev)}


def create(term, line, block):
    return [Dockerfile(is_dev=term.tag == "dockerfile-dev")]


@reduce(Dockerfile, resource_id="leap_mn.pipdependency")
def add_pip_dependency(dockerfile, pip_dependency):
    if pip_dependency.is_dev and not dockerfile.is_dev:
        return

    if dockerfile.is_mentioned_in_same_block(pip_dependency):
        if pip_dependency.package_name not in dockerfile.pip_package_names:
            dockerfile.pip_package_names.append(pip_dependency.package_name)


tags = ["dockerfile", "dockerfile-dev"]
