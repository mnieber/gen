from pathlib import Path

from moonleap import add
from titan.react_pkg.nodepackage import load_node_package_config


def use_packages(self, package_names):
    root_dir = Path(__file__).parent.parent

    for package_name in package_names:
        package_dir = root_dir / "packages" / package_name
        package_json = package_dir / "package.json"
        if package_json.exists():
            add(self, load_node_package_config(package_json))

        files_dir = package_dir / "files"
        if files_dir.exists():
            self.add_template_dir(
                root_dir / "__init__.py", files_dir.relative_to(root_dir)
            )
