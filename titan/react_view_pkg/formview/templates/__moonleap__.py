import ramda as R
from moonleap.utils.case import u0


def get_helpers(_):
    class Helpers:
        form_view = _.component
        mutation = form_view.mutation
        scalar_field_specs = [
            x for x in mutation.gql_spec.get_inputs() if x.field_type != "form"
        ]
        form_field_specs = [x for x in mutation.gql_spec.get_inputs(["form"])]
        fields = []

        def __init__(self):
            self.fields.extend([(x.name, x) for x in self.scalar_field_specs])
            for form_field_spec in self.form_field_specs:
                self.fields.extend(
                    [
                        (f"{form_field_spec.name}.{x.name}", x)
                        for x in self._form_fields(form_field_spec)
                    ]
                )

        def _form_fields(self, form_field_spec):
            return [
                x
                for x in form_field_spec.target_type_spec.get_field_specs()
                if "client" in x.has_model
            ]

        def slug_src(self, field_spec):
            slug_sources = [
                field_spec.name
                for prefix, field_spec in self.fields
                if field_spec.is_slug_src
            ]
            return R.head(slug_sources) or "Moonleap Todo: slug_src"

        def label(self, name):
            return u0(name.replace(".", " "))

        def display_field_name(self, type_spec):
            return type_spec.display_field.name if type_spec.display_field else "id"

    return Helpers()
