from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict()

    return LayerConfig(lambda x: inner())
