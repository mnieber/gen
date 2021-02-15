from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict(
            ROOT=dict(decorators=dict(docker=["make"])),
            MAKE=dict(cwd=r"${/SERVER/src_dir}"),
        )

    return LayerConfig(lambda x: inner())
