from moonleap import u0
from titan.typespec.api_spec import ApiSpec
from titan.typespec.field_spec import FieldSpec
from titan.typespec.type_spec import TypeSpec

from .load_type_specs.field_spec_from_dict import field_spec_from_dict


def get_api_spec(api_reg, host, endpoint_key, endpoint_spec_dict, known_type_names):
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
        field_spec = field_spec_data["field_spec"]
        _check_field_spec(field_spec, known_type_names)

        inputs.append(field_spec)

    outputs = []
    for key, field_spec_value in endpoint_spec_dict.get("outputs", {}).items():
        field_spec_data = field_spec_from_dict(host, key, field_spec_value)
        outputs.append(field_spec_data["field_spec"])

    deletes = []
    for item_name in endpoint_spec_dict.get("deletes", []):
        is_list = item_name.endswith("Set")
        deletes.append((item_name.removesuffix("Set"), is_list))

    orders = [x.split(".") for x in endpoint_spec_dict.get("orders", [])]
    for x in orders:
        x[0] = u0(x[0])

    saves = []
    for item_name in endpoint_spec_dict.get("saves", []):
        is_list = item_name.endswith("Set")
        saves.append((item_name.removesuffix("Set"), is_list))

    invalidates = endpoint_spec_dict.get("invalidates", [])
    is_stub = endpoint_spec_dict.get("isStub", False)

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

    api_reg.setdefault(
        name,
        ApiSpec(
            name=name,
            is_mutation=is_mutation,
            deletes=deletes,
            orders=orders,
            saves=saves,
            invalidates=invalidates,
            is_stub=is_stub,
            inputs_type_spec=TypeSpec(type_name=name + "Inputs", field_specs=inputs),
            outputs_type_spec=TypeSpec(type_name=name + "Outputs", field_specs=outputs),
        ),
    )


def _check_field_spec(field_spec, known_type_names):
    if field_spec.field_type in ("fk", "relatedSet", "form", "uuid[]", "uuid"):
        if field_spec.target not in known_type_names:
            raise Exception(
                f"Unknown type {field_spec.target} for field {field_spec.name}"
            )
