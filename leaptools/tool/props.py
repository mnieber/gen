import ramda as R
from moonleap.resource.slctrs import PropSelector, Selector


def get_pip_pkg_names():
    return _list_of_package_names(lambda tool: tool.pip_dependencies.merged)


def get_pkg_names():
    return _list_of_package_names(lambda tool: tool.pkg_dependencies.merged)


def _list_of_package_names(get_pkgs):
    def f(self, is_dev=False):
        fltr = R.filter(lambda x: x.is_dev == is_dev)
        slctr = Selector(
            [
                PropSelector(lambda x: x.tools),
                PropSelector(get_pkgs, fltr=fltr),
                PropSelector(lambda x: x.package_names),
            ]
        )
        return slctr.select_from(self)

    return f


def get_makefile_rules():
    slctr = Selector(
        [
            PropSelector(lambda x: x.tools),
            PropSelector(lambda x: x.makefile_rules),
        ]
    )

    def getter(self):
        return slctr.select_from(self)

    return getter


def add_tool(self, tool):
    self.add_to_tools(tool)
    self.layer_configs.add_source(tool)
    self.docker_compose_configs.add_source(tool)
    tool.output_paths.add_source(self)
