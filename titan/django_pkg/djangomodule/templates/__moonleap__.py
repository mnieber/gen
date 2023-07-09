from moonleap.utils.inflect import plural


def get_helpers(_):
    class Helpers:
        django_app = _.module.django_app
        django_models = _.module.django_models
        translations = []

        def __init__(self):
            if self.django_app.use_translation:
                self._init_translations()

        def _init_translations(self):
            for django_model in self.django_models:
                name = django_model.kebab_name
                self.django_app.add_translation(name, name, self.translations)
                self.django_app.add_translation(
                    plural(name), plural(name), self.translations
                )
            self.translations = sorted(self.translations)

    return Helpers()
