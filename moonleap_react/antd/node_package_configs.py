from moonleap_react.nodepackage import NodePackageConfig


def get():
    return NodePackageConfig(
        body={
            "dependencies": {
                "@ant-design/icons": "^4.2.2",
                "antd": "^4.6.5",
            },
        }
    )
