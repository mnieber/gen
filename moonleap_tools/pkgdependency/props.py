from moonleap_tools.pipdependency.props import list_of_package_names


def get_pkg_names():
    return list_of_package_names(lambda tool: tool.pkg_dependencies.merged)
