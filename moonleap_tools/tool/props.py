from moonleap.parser.term import term_to_word
from moonleap.resource.slctrs import PropSelector, Selector


def get_pip_pkg_names():
    return _list_of_package_names(lambda tool: tool.pip_dependencies.merged)


def get_pip_requirements():
    return _list_of_package_names(
        lambda tool: tool.pip_requirements.merged, add_via=False
    )


def get_pkg_names():
    return _list_of_package_names(lambda tool: tool.pkg_dependencies.merged)


def _list_of_package_names(get_pkgs, add_via=True):
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
                                + (
                                    f"` # via {term_to_word(tool.term)}`"
                                    if add_via
                                    else ""
                                )
                            )
        return result

    return f


def get_makefile_rules():
    slctr = Selector(
        [
            PropSelector(lambda x: x.tools),
            PropSelector(lambda x: x.makefile_rules.merged),
        ]
    )

    def getter(self):
        return slctr.select_from(self)

    return getter
