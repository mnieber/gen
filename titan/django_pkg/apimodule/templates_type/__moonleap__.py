from titan.api_pkg.typeregistry import get_type_reg


def get_helpers(_):
    class Helpers:
        type_reg = get_type_reg()
        item_list = _.item.item_list
        django_module = item_list.django_module
        type_spec = _.item.type_spec
        model_field_specs = [
            x for x in _.item.type_spec.get_field_specs() if not x.derived
        ]
        derived_field_specs = [
            x
            for x in _.item.type_spec.get_field_specs()
            if x.derived and "server" in x.api
        ]
        form_field_specs = []

        @property
        def excluded_field_specs(self):
            derived_field_names = [x.name for x in self.derived_field_specs]
            result = [
                field_spec
                for field_spec in self.model_field_specs
                if "server" not in field_spec.api
                and field_spec.name not in derived_field_names
            ]
            return result

    return Helpers()
