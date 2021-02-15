from moonleap_dodo.layer import LayerConfig


def get():
    def inner():
        return dict(
            ROOT=dict(
                aliases=dict(install=r"install-packages --pip-requirements default"),
                decorators=dict(docker=["install-packages"]),
            ),
            SERVER=dict(pip_requirements=r"${/SERVER/src_dir}/requirements.dev.txt"),
        )

    return LayerConfig(lambda x: inner())
