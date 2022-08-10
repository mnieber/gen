from pathlib import Path


def use_packages(self, package_names, packages_dir=None):
    packages_dir = packages_dir or Path(__file__).parent.parent / "packages"

    for package_name in package_names:
        package_dir = packages_dir / package_name

        files_dir = package_dir / "files"
        if files_dir.exists():
            # TODO
            # add template dir(packages_dir / files_dir.relative_to(packages_dir))
            pass
