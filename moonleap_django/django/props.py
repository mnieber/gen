import ramda as R
from moonleap.utils.merge_into_config import merge_into_config
from moonleap_django.django.resources import DjangoConfig


def settings(self):
    def _merge(lhs, rhs):
        new_body = dict()
        merge_into_config(new_body, lhs.values)
        merge_into_config(new_body, rhs.values)
        return DjangoConfig(new_body)

    return R.reduce(_merge, DjangoConfig({}), self.django_configs.merged)


def get_settings_or(self, default, path):
    return R.path_or(default, path, self.settings.values)
