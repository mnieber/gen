import ramda as R
from moonleap.utils.merge_into_config import merge_into_config
from titan.django_pkg.djangoapp.resources import DjangoConfig


def config(self):
    def _merge(lhs, rhs):
        settings = dict()
        merge_into_config(settings, lhs.settings)
        merge_into_config(settings, rhs.settings)
        return DjangoConfig(
            settings=settings,
            urls=sorted(R.uniq(lhs.urls + rhs.urls)),
            urls_imports=R.uniq(lhs.urls_imports + rhs.urls_imports),
            cors_urls=sorted(R.uniq(lhs.cors_urls + rhs.cors_urls)),
        )

    return R.reduce(_merge, DjangoConfig({}), self.django_configs.merged)


def get_setting_or(self, default, path):
    return R.path_or(default, path, self.config.settings)


def third_party_apps(self):
    return sorted(self.get_setting_or([], ["installed_apps", "THIRD_PARTY_APPS"]))


def local_apps(self):
    return sorted(self.get_setting_or([], ["installed_apps", "LOCAL_APPS"]))


def cors_urls_regex(self):
    return "|".join(self.config.cors_urls)
