from moonleap.gqlspec.gql_spec import GqlSpec
from moonleap.typespec.field_spec import FieldSpec
from moonleap.typespec.load_type_specs.get_field_spec import get_field_spec
from moonleap.typespec.type_spec import TypeSpec


def get_gql_spec(gql_spec_store, type_spec_store, endpoint_key, endpoint_spec_dict):
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
        field_spec = get_field_spec(
            type_spec_store, key, field_spec_value, None, first_pass=True
        )
        inputs.append(field_spec)

    outputs = []
    for key, field_spec_value in endpoint_spec_dict.get("outputs", {}).items():
        field_spec = get_field_spec(
            type_spec_store, key, field_spec_value, None, first_pass=True
        )
        outputs.append(field_spec)

    deletes = []
    for item_name in endpoint_spec_dict.get("deletes", []):
        is_list = item_name.endswith("Set")
        deletes.append((item_name.removesuffix("Set"), is_list))

    saves = []
    for item_name in endpoint_spec_dict.get("saves", []):
        is_list = item_name.endswith("Set")
        saves.append((item_name.removesuffix("Set"), is_list))

    if is_mutation:
        outputs.append(
            FieldSpec(
                name="success",
                required=False,
                field_type="boolean",
            )
        )

        outputs.append(
            FieldSpec(
                name="errors",
                required=False,
                field_type="any",
            )
        )

    gql_spec_store.setdefault(
        name,
        GqlSpec(
            name=name,
            is_mutation=is_mutation,
            deletes=deletes,
            saves=saves,
            inputs_type_spec=TypeSpec(type_name=name + "Inputs", field_specs=inputs),
            outputs_type_spec=TypeSpec(type_name=name + "Outputs", field_specs=outputs),
        ),
    )