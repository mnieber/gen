from titan.dodo_pkg.layer import LayerConfig


def get():
    def inner():
        return dict(
            ROOT=dict(
                aliases=dict(
                    install=r"make install",
                    serve=r"make runserver",
                ),
                decorators=dict(docker=["make"]),
            ),
            NODE=dict(node_modules_dir="${/SERVER/src_dir}/node_modules"),
        )

    return LayerConfig(lambda x: inner())
