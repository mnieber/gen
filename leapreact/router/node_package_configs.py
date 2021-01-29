from leapreact.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "devDependencies": {
                "history": "^4.10.1",
                "react-router-dom": "^5.2.0",
            },
        }
    )
