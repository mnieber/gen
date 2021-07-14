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


def get_for_project(service_name):
    def inner():
        return dict(
            MENU=dict(
                #
                commands=dict(
                    #
                    serve=[f"dodo {service_name}.serve"]
                )
            ),
        )

    return LayerConfig(lambda x: inner())
