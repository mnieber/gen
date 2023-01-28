from moonleap.utils.case import sn
from moonleap.utils.fp import append_uniq
from moonleap.utils.inflect import plural
from titan.django_pkg.djangomodel.sort_django_models import sort_django_models


def get_helpers(_):
    class Helpers:
        django_app = _.module.django_app

        django_models = sort_django_models(_.module.django_models)
        translations = []

        def __init__(self):
            if self.django_app.use_translation:
                self._init_translations()

        def fields(self, model):
            return [
                x
                for x in model.fields
                if not (model.type_spec.is_entity and x.name in ("id", "created"))
            ]

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
        def type_specs_to_import(self):
            result = []
            for django_model in self.django_models:
                for field_spec in django_model.type_spec.get_field_specs(
                    ["fk", "relatedSet"]
                ):
                    type_spec = field_spec.target_type_spec
                    if type_spec.django_module is not _.module:
                        append_uniq(result, type_spec)
            return result

        def display_field_expr(self, django_model):
            if django_model.type_spec.display_field:
                display_field_name = sn(django_model.type_spec.display_field.name)
                return f"str(self.{display_field_name})"
            return "str(self.id)"

    return Helpers()
