import ramda as R

from moonleap.utils.case import u0


def get_helpers(_):
    class Helpers:
        form_view = _.component
        mutation = form_view.mutation
        scalar_field_specs = [
            x for x in mutation.api_spec.get_inputs() if x.field_type != "form"
        ]
        fields = []
        uuid_fields = []
        validated_fields = []

        def __init__(self):
            self._get_fields()
            self._get_validated_fields()

        def _get_fields(self):
            self.fields.extend([(x.name, x) for x in self.scalar_field_specs])
            for form_field_spec in self.mutation.api_spec.get_inputs(["form"]):
                self.fields.extend(
                    [
                        (f"{form_field_spec.name}.{x.name}", x)
                        for x in self._form_fields(form_field_spec)
                        if not (x.field_type == "uuid" and not x.target)
                    ]
                )
            self.uuid_fields = [
                x for x in self.fields if x[1].field_type == "uuid" and x[1].target
            ]

        def _get_validated_fields(self):
            for name, field_spec in self.fields:
                if (
                    not field_spec.is_optional("client")
                    and not field_spec.field_type == "boolean"
                ):
                    self.validated_fields.append((name, field_spec))

        def _form_fields(self, form_field_spec):
            return [
                x
                for x in form_field_spec.target_type_spec.get_field_specs()
                if "client" in x.has_model
            ]

        def slug_src(self, field_spec):
            slug_sources = [
                name for name, field_spec in self.fields if field_spec.is_slug_src
            ]
            return R.head(slug_sources) or "Moonleap Todo: slug_src"

        def label(self, name):
            return u0(name.replace(".", " "))

        def display_field_name(self, type_spec):
            return type_spec.display_field.name if type_spec.display_field else "id"

        def initial_value(self, field_spec):
            if field_spec.field_type == "boolean":
                return "false"
            return "null"

    return Helpers()
