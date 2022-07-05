from titan.dodo_pkg.layer import LayerConfig


def get():
    def inner():
        return dict(
            ROOT=dict(
                aliases=dict(serve="make run-server"),
                decorators=dict(docker=["django-manage"]),
            ),
            DJANGO=dict(cwd="${/SERVER/src_dir}", python="python"),
        )

    return LayerConfig(lambda x: inner())
