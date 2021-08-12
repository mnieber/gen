def list_of_package_names(get_pkgs, add_via=True):
    def f(self, is_dev=False):
        result = []
        pkg_names = []

        for tool in self.tools:
            for pkg in get_pkgs(tool):
                if pkg.is_dev == is_dev:
                    for pkg_name in pkg.package_names:
                        if pkg_name not in pkg_names:
                            pkg_names.append(pkg_name)
                            result.append(
                                fr"{pkg_name.ljust(20)}"
                                + (f"` # via {tool.name}`" if add_via else "")
                            )
        return sorted(result)

    return f


def get_pip_pkg_names():
    return list_of_package_names(lambda tool: tool.pip_dependencies.merged)


def get_pip_requirements():
    return list_of_package_names(
        lambda tool: tool.pip_requirements.merged, add_via=False
    )
