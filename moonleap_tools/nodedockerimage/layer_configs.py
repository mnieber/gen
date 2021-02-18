from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict(
            ROOT=dict(
                aliases=dict(
                    install=r"install-packages --node-modules default",
                    serve=r"yarn start",
                ),
                decorators=dict(docker=["install-packages", "yarn"]),
            ),
            NODE=dict(
                cwd=r"${/SERVER/src_dir}",
                node_modules_dir=r"${/SERVER/src_dir}/node_modules",
            ),
        )

    return LayerConfig(lambda x: inner())
