from moonleap_react.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "dependencies": {
                "history": "^4.10.1",
                "@types/react-router-dom": "^5.1.6",
                "react-router-dom": "^5.2.0",
            },
        }
    )
