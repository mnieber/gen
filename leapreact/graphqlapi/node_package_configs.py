from leapreact.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "dependencies": {
                "graphql": "^15.4.0",
                "graphql-request": "^3.4.0",
            },
        }
    )
