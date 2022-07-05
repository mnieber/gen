import typing as T

from moonleap import get_session


def list_of_package_names(get_pkgs, add_via: T.Any = False):
    def f(self, is_dev=False):
        nonlocal add_via
        result = []
        pkg_names = []

        if add_via is None:
            add_via = get_session().settings.get("add_via", False)

        for tool in self.tools:
            for pkg in get_pkgs(tool):
                if pkg.is_dev == is_dev:
                    for pkg_name in pkg.package_names:
                        if pkg_name not in pkg_names:
                            pkg_names.append(pkg_name)
                            result.append(
                                fr"{pkg_name.ljust(20 if add_via else 0)}"
                                + (f"` # via {tool.name}`" if add_via else "")
                            )
        return sorted(result)

    return f


def get_pip_pkg_names():
    return list_of_package_names(
        lambda tool: tool.pip_dependencies.merged, add_via=None
    )


def get_pip_requirements():
    return list_of_package_names(
        lambda tool: tool.pip_requirements.merged, add_via=False
    )
