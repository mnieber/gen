from titan.tools_pkg.optdir import OptPath

pytest_html_opt_path = OptPath(
    is_dir=False,
    from_path="pytest_report.html",
    to_path="/app/pytest_report.html",
)

pytest_html_asset_path = OptPath(
    is_dir=True,
    from_path="assets",
    to_path="/app/assets",
)
