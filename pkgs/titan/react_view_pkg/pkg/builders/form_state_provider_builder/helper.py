from titan.types_pkg.typeregistry import get_type_reg

from moonleap import u0


class Helper:
    def __init__(self, item_name, mutation):
        self.item_name = item_name
        self.type_spec = get_type_reg().get(u0(self.item_name) + "Form")
        self.mutation = mutation.api_spec
        self.fields = get_fields(self.mutation) if self.mutation else []
        self.uuid_fields = [
            x for x in self.fields if x[1].field_type == "uuid" and x[1].target
        ]
        self.validated_fields = Helper._get_validated_fields(self.fields)

    def initial_value(self, field_spec):
        if field_spec.field_type == "boolean":
            return "false"
        return "null"

    @staticmethod
    def _get_validated_fields(fields):
        result = []
        for name, field_spec in fields:
            if (
                not field_spec.is_optional("client")
                and not field_spec.field_type == "boolean"
            ):
                result.append((name, field_spec))
        return result


def get_fields(mutation):
    scalar_field_specs = [x for x in mutation.get_inputs() if x.field_type != "form"]
    fields = []
    fields.extend([(x.name, x) for x in scalar_field_specs])
    for form_field_spec in mutation.get_inputs(["form"]):
        fields.extend(
            [
                (f"{form_field_spec.name}.{x.name}", x)
                for x in _form_fields(form_field_spec)
                if not (x.field_type == "uuid" and not x.target)
            ]
        )
    return fields


def _form_fields(form_field_spec):
    return [
        x
        for x in form_field_spec.target_type_spec.get_field_specs()
        if "client" in x.has_model
    ]
