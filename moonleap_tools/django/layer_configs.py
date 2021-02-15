from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict(ROOT=dict(aliases=dict(serve="make runserver")))

    return LayerConfig(lambda x: inner())
