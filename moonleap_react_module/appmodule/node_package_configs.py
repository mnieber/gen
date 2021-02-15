from moonleap_react.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "dependencies": {
                "jquery": "^3.1.1",
                "lodash": "^4.17.20",
                "micro-signals": "^2.1.0",
                "mobx": "^5.14.0",
                "mobx-react": "^6.1.4",
            },
        }
    )
