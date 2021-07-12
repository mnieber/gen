from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict(
            ROOT=dict(
                aliases=dict(
                    install=r"make install",
                    serve=r"make runserver",
                ),
                decorators=dict(docker=["make"]),
            )
        )

    return LayerConfig(lambda x: inner())
