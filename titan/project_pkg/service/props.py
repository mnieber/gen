from moonleap import get_session


def get_tweak_or(self, default_value, rel_path):
    return get_session().get_tweak_or(default_value, ["services", self.name, *rel_path])
