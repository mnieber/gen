from moonleap.resources.field_spec import FieldSpec
from moonleap.resources.type_spec_store import TypeSpec


def default_outputs_type_spec(self, name):
    return TypeSpec(
        type_name=name,
        field_specs=[
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
    )
