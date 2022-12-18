from pathlib import Path

from moonleap import Resource


def use_react_package(res, package_name, output_dir=None, packages_dir=None):
    packages_dir = Path(packages_dir) if packages_dir else Path(__file__).parent
    package_dir = packages_dir / package_name

    if package_dir.exists():
        if not _renders(res, package_dir):
            res.renders(
                [Resource()],
                output_dir or "",
                dict(),
                [package_dir],
            )


def _renders(res, files_dir):
    for render_task in res.render_tasks:
        for template_dir in render_task.template_dirs:
            if template_dir == files_dir:
                return True
    return False
