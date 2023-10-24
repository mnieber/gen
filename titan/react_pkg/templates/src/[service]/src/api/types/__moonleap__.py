from moonleap import l0
from titan.api_pkg.apiregistry.get_public_type_specs import get_public_type_specs
from titan.types_pkg.typeregistry import get_type_reg


def get_helpers(_):
    class Helpers:
        form_field_specs = (
            [x for x in _.form_type_spec.get_field_specs() if x.has_model]
            if _.form_type_spec
            else []
        )
        item = get_type_reg().get_item(l0(_.type_spec.type_name))

    return Helpers()


def get_meta_data_by_fn(_, __):
    return {
        "type.ts.j2": {
            "name": f"{_.type_spec.type_name}T.ts",
        }
    }


def get_contexts(_):
    return [
        dict(
            type_spec=type_spec,
            form_type_spec=_.type_reg.get(type_spec.type_name + "Form", None),
        )
        for type_spec in get_public_type_specs(
            _.api_reg,
            include_stubs=True,
            predicate=lambda type_spec: not type_spec.no_api,
        )
    ]
