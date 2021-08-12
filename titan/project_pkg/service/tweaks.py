import ramda as R
from moonleap import get_session


def tweak(service):
    tweaks = R.path_or({}, ["services", service.name])(get_session().get_tweaks())

    def get_tweak(prop, default_value=None):
        return tweaks.get(prop, default_value)

    if get_tweak("port"):
        service.port = get_tweak("port")
