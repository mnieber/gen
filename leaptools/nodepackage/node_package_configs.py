from .resources import NodePackageConfig


def get(node_package):
    def inner():
        return {
            "name": node_package.service.name,
            "version": "0.1.0",
            "private": True,
            "dependencies": {},
        }

    return NodePackageConfig(lambda x: inner())
