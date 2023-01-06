from titan.django_pkg.djangomodel.sort_django_models import sort_django_models
from titan.types_pkg.typeregistry import get_type_reg

from moonleap import u0
from moonleap.utils.case import sn


def get_helpers(_):
    class Helpers:
        data = []

        def __init__(self):
            self.data = self.get_data()

        def get_data(self):
            result = []
            for django_model in sort_django_models(_.module.django_models):
                item_list = django_model.item_list
                type_spec = django_model.type_spec
                data = dict(
                    type_spec=type_spec,
                    create_inline_model=self.get_create_inline_model(type_spec),
                    inline_model_fields=self.get_inline_model_fields(type_spec),
                    excluded_model_fields=self.get_excluded_model_fields(type_spec),
                    has_sortable_inlines=bool(self.get_sortable_inlines(type_spec)),
                    autocomplete_fields=self.get_autocomplete_fields(type_spec),
                    search_by=type_spec.admin_search_by,
                )
                result.append((item_list, data))
            return result

        def get_create_inline_model(self, type_spec):
            for parent_type_spec in get_type_reg().type_specs():
                for field_spec in parent_type_spec.get_field_specs(["relatedSet"]):
                    if (
                        field_spec.admin_inline
                        and field_spec.target == type_spec.type_name
                    ):
                        return True
            return False

        def get_inline_model_fields(self, type_spec):
            return [
                x for x in type_spec.get_field_specs(["relatedSet"]) if x.admin_inline
            ]

        def get_excluded_model_fields(self, type_spec):
            return [x for x in type_spec.get_field_specs() if not x.admin]

        def get_autocomplete_fields(self, type_spec):
            return [
                sn(x.name)
                for x in type_spec.get_field_specs(["relatedSet"])
                if x.target_type_spec.admin_search_by
            ]

        def get_sortable_inlines(self, type_spec):
            return [
                x
                for x in self.get_inline_model_fields(type_spec)
                if x.target_type_spec.is_sorted
            ]

        @property
        def type_specs_to_import(self):
            result = []
            for dummy, data in self.data:
                for inline_model_field in data["inline_model_fields"]:
                    type_spec = inline_model_field.target_type_spec
                    if type_spec not in result:
                        if not (type_spec.django_module is _.module):
                            result.append(type_spec)
            return result

    return Helpers()
