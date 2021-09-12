from titan.dodo_pkg.layer import LayerConfig


def get():
    def inner():
        return dict()

    return LayerConfig(lambda x: inner())
