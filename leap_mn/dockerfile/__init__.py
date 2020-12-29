from leap_mn.resource import Resource


class Dockerfile(Resource):
    def __init__(self, name):
        self.name = name

    def describe(self):
        return {str(self): dict(name=self.name)}


def create(term, line, block):
    return Dockerfile("default")


def create_dev(term, line, block):
    return Dockerfile("dev")


create_rule_by_tag = {
    "docker-file-dev": create_dev,
    "docker-file": create,
}


def pip_install_in_dockerfile(block, pip_package, try_resource_tags):
    for resource_tag in try_resource_tags:
        dockerfile = block.get_resource_by_tag(resource_tag)
        if dockerfile:
            dockerfile.add_pip_install(pip_package)
            return
