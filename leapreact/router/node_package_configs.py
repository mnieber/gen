from leapreact.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "devDependencies": {
                "react-router-dom": "^5.2.0",
            },
        }
    )
