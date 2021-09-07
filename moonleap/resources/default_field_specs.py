from moonleap.resources.field_spec import FieldSpec

default_field_specs = [
    FieldSpec(
        name_snake="id",
        name="id",
        required=True,
        private=False,
        field_type="uuid",
    ),
    FieldSpec(
        name_snake="name",
        name="name",
        required=True,
        private=False,
        field_type="string",
    ),
]
