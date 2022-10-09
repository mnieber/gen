from moonleap.typespec.field_spec import FieldSpec

default_field_specs = [
    FieldSpec(key="id", field_type="uuid", required=True),
    FieldSpec(key="name", field_type="string", required=True),
]


class DefaultFieldSpecsStore:
    def __init__(self):
        self._field_specs = {}

    def register_field_spec(self, type_name, field_spec):
        for default_field_spec in self.get_field_specs(type_name):
            if default_field_spec.key == field_spec.key:
                if default_field_spec.field_type == field_spec.field_type:
                    return
                raise Exception(
                    f"Error: trying to register a default field spec ({field_spec.key})"
                    + f" that already exists for type {type_name}."
                )

        self._field_specs.setdefault(type_name, []).append(field_spec)

    def get_field_specs(self, type_name):
        field_specs = list(default_field_specs) + self._field_specs.get(type_name, [])
        return sorted(field_specs, key=lambda x: x.key)
