from titan.types_pkg.pkg.field_spec import FieldSpec
from titan.types_pkg.pkg.load_type_specs.field_spec_from_dict import (
    field_spec_from_dict,
)
from titan.types_pkg.pkg.type_spec import TypeSpec

from .gql_spec import GqlSpec


def get_gql_spec(gql_reg, host, endpoint_key, endpoint_spec_dict):
    parts = endpoint_key.split()
    if not parts:
        raise Exception("Invalid endpoint key: " + endpoint_key)

    endpoint_type = parts.pop(0)
    is_mutation = endpoint_type == "mutation"
    is_query = endpoint_type == "query"
    if not is_mutation and not is_query:
        raise Exception(f"Invalid endpoint key: {endpoint_key}")

    name = parts.pop(0)

    inputs = []
    for key, field_spec_value in endpoint_spec_dict.get("inputs", {}).items():
        field_spec_data = field_spec_from_dict(host, key, field_spec_value)
        inputs.append(field_spec_data["field_spec"])

    outputs = []
    for key, field_spec_value in endpoint_spec_dict.get("outputs", {}).items():
        field_spec_data = field_spec_from_dict(host, key, field_spec_value)
        outputs.append(field_spec_data["field_spec"])

    deletes = []
    for item_name in endpoint_spec_dict.get("deletes", []):
        is_list = item_name.endswith("Set")
        deletes.append((item_name.removesuffix("Set"), is_list))

    saves = []
    for item_name in endpoint_spec_dict.get("saves", []):
        is_list = item_name.endswith("Set")
        saves.append((item_name.removesuffix("Set"), is_list))

    invalidates = endpoint_spec_dict.get("invalidates", [])

    if is_mutation:
        outputs.append(
            FieldSpec(
                key="success",
                field_type="boolean",
                has_api=[host],
            )
        )

        outputs.append(
            FieldSpec(
                key="errors",
                field_type="any",
                has_api=[host],
            )
        )

    gql_reg.setdefault(
        name,
        GqlSpec(
            name=name,
            is_mutation=is_mutation,
            deletes=deletes,
            saves=saves,
            invalidates=invalidates,
            inputs_type_spec=TypeSpec(type_name=name + "Inputs", field_specs=inputs),
            outputs_type_spec=TypeSpec(type_name=name + "Outputs", field_specs=outputs),
        ),
    )
