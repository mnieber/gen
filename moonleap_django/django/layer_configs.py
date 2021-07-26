from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict(
            ROOT=dict(
                aliases=dict(serve="make runserver"),
                decorators=dict(docker=["django-manage"]),
            ),
            DJANGO=dict(cwd="${/SERVER/src_dir}", python="python"),
        )

    return LayerConfig(lambda x: inner())
