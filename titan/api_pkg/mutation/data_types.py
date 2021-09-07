import ramda as R
from moonleap.resources.data_type_spec_store import DataTypeField, DataTypeSpec

mutation_output_data_type = DataTypeSpec(
    type_name="MutationOutputType",
    field_by_name=R.index_by(
        R.prop("name"),
        [
            DataTypeField(
                name_snake="success",
                name="success",
                required=False,
                private=False,
                field_type="boolean",
            ),
            DataTypeField(
                name_snake="errors",
                name="errors",
                required=False,
                private=False,
                field_type="any",
            ),
        ],
    ),
)
