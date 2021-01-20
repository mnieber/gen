from leapdodo.layer import LayerConfig


def get():
    def l():
        return dict(
            ROOT=dict(decorators=dict(docker=["make"])),
            MAKE=dict(cwd=r"${/SERVER/src_dir}"),
        )

    return LayerConfig(lambda x: l())
