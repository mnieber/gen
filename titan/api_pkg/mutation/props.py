import ramda as R
from moonleap.resources.data_type_spec_store import (
    DataTypeField,
    DataTypeSpec,
    data_type_spec_store,
)

default_mutation_output_data_type = DataTypeSpec(
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


def posts_item(self, item_name):
    return [x for x in self.items_posted if x.item_name == item_name]


def data_type_out(self):
    name = f"{self.name}OutputType"
    return data_type_spec_store.spec_by_name.get(
        name, default_mutation_output_data_type
    )
