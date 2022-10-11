from moonleap.utils.fp import add_to_list_as_set
from moonleap.utils.inflect import plural
from titan.django_pkg.djangomodel.sort_django_models import sort_django_models


def get_helpers(_):
    class Helpers:
        django_app = _.module.django_app

        django_models = sort_django_models(_.module.django_models)
        translations = []

        def __init__(self):
            self._init_translations()

        def _init_translations(self):
            for django_model in self.django_models:
                name = django_model.kebab_name
                self.django_app.add_translation(name, name, self.translations)
                self.django_app.add_translation(
                    plural(name), plural(name), self.translations
                )
                for model_field in django_model.fields:
                    self.django_app.add_translation(
                        model_field.translation_id, model_field.name, self.translations
                    )
            self.translations = sorted(self.translations)

        @property
        def items_to_import(self):
            result = []
            for django_model in self.django_models:
                for field_spec in django_model.type_spec.get_field_specs(
                    ["fk", "relatedSet"]
                ):
                    item = field_spec.target_item
                    if item.django_module is not _.module:
                        add_to_list_as_set(result, item)
            return result

    return Helpers()
