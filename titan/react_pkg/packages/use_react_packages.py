from pathlib import Path

from moonleap import Resource


def use_react_packages(res, package_names, packages_dir=None):
    packages_dir = packages_dir or Path(__file__).parent

    for package_name in package_names:
        package_dir = packages_dir / package_name

        files_dir = package_dir / "files"
        if files_dir.exists():
            if not _renders(res, files_dir):
                res.renders(
                    [Resource()],
                    "",
                    dict(),
                    [files_dir],
                )


def _renders(res, files_dir):
    for render_task in res.render_tasks:
        for template_dir in render_task.template_dirs:
            if template_dir == files_dir:
                return True
    return False
