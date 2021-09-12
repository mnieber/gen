from titan.dodo_pkg.layer import LayerConfig


def get_pytest_options(pytest):
    def inner():
        return dict(
            PYTEST=dict(capture=False, cwd=r"${/SERVER/src_dir}"),
            ROOT=dict(decorators=dict(docker=["pytest"])),
        )

    return LayerConfig(lambda x: inner())


def get_pytest_html_options(pytest_html):
    def inner():
        result = dict(html_report=r"${/SERVER/install_dir}/pytest_report.html")
        return dict(PYTEST=result)

    return LayerConfig(lambda x: inner())
