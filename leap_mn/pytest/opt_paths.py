from leap_mn.optdir import OptPath

pytest_opt_path = OptPath(
    is_dir=False,
    from_path="foo.html",
    to_path="foo.html",
)

pytest_html_opt_path = OptPath(
    is_dir=False,
    from_path="pytest_report.html",
    to_path="/home/root/pytest_report.html",
)
