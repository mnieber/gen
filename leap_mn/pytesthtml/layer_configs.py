def get_pytest_html_options(pytest_html):
    result = dict(html_report=r"${/SERVER/install_dir}/report.html")
    return dict(PYTEST=result)
