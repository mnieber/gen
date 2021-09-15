import ramda as R
from moonleap.resources.type_spec_store import FieldSpec, TypeSpec, type_spec_store


def _default_inputs_type_spec(name):
    return TypeSpec(
        type_name=name,
        field_spec_by_name={},
    )


def _default_outputs_type_spec(name):
    return TypeSpec(
        type_name=name,
        field_spec_by_name=R.index_by(
            R.prop("name"),
            [
                FieldSpec(
                    name_snake="success",
                    name="success",
                    required=False,
                    private=False,
                    field_type="boolean",
                ),
                FieldSpec(
                    name_snake="errors",
                    name="errors",
                    required=False,
                    private=False,
                    field_type="any",
                ),
            ],
        ),
    )


def inputs_type_spec(self):
    name = f"{self.name}InputType"
    return type_spec_store.get(name) or _default_inputs_type_spec(name)


def outputs_type_spec(self):
    name = f"{self.name}OutputType"
    return type_spec_store.get(name, None) or _default_outputs_type_spec(name)
