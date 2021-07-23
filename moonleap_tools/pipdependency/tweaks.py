import ramda as R
from moonleap import add, get_session
from moonleap_tools.pipdependency.resources import PipDependency, PipRequirement
from moonleap_tools.pkgdependency import PkgDependency


def tweak_service(service):
    tweaks = R.path_or({}, ["services", service.name])(get_session().get_tweaks())

    def get_tweak(prop, default_value=None):
        return tweaks.get(prop, default_value)

    if service.dockerfile:
        if get_tweak("pkg_dependencies"):
            add(
                service.dockerfile,
                PkgDependency(package_names=get_tweak("pkg_dependencies")),
            )

        if get_tweak("pkg_dependencies_dev"):
            add(
                service.dockerfile,
                PkgDependency(
                    package_names=get_tweak("pkg_dependencies_dev"), is_dev=True
                ),
            )

        if get_tweak("pip_dependencies"):
            add(
                service.dockerfile,
                PipDependency(package_names=get_tweak("pip_dependencies")),
            )

        if get_tweak("pip_dependencies_dev"):
            add(
                service.dockerfile,
                PipDependency(
                    package_names=get_tweak("pip_dependencies_dev"), is_dev=True
                ),
            )

        if get_tweak("pip_requirements"):
            add(
                service.dockerfile,
                PipRequirement(package_names=get_tweak("pip_requirements")),
            )

        if get_tweak("pip_requirements_dev"):
            add(
                service.dockerfile,
                PipRequirement(
                    package_names=get_tweak("pip_requirements_dev"), is_dev=True
                ),
            )
