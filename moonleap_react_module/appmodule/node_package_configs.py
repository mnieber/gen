from moonleap_react.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "dependencies": {
                "@types/classnames": "^2.2.11",
                "classnames": "^2.2.6",
                "jquery": "^3.1.1",
                "@types/lodash": "^4.14.165",
                "lodash": "^4.17.20",
                "micro-signals": "^2.1.0",
                "mobx-react-lite": "^3.1.6",
                "mobx": "^6.0.4",
                "use-deep-compare-effect": "^1.6.1",
            },
        }
    )
