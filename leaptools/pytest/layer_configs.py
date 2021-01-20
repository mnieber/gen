from leapdodo.layer import LayerConfig


def get_pytest_options(pytest):
    def l():
        result = dict(capture=False)

        if pytest.service and pytest.service.src_dir:
            result["src_dir"] = pytest.service.src_dir.location

        return dict(PYTEST=result)

    return LayerConfig(lambda x: l())


def get_pytest_html_options(pytest_html):
    def l():
        result = dict(html_report=r"${/SERVER/install_dir}/report.html")
        return dict(PYTEST=result)

    return LayerConfig(lambda x: l())
