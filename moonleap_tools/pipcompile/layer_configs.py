from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict(ROOT=dict(aliases={"pip-compile": "make pip-compile"}))

    return LayerConfig(lambda x: inner())
