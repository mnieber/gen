import typing as T

from typespec.api_spec import ApiSpec


def get_fields(mutation: ApiSpec, field_names: list[str]):
    scalar_field_specs = [x for x in mutation.get_inputs() if x.field_type != "form"]
    form_field_specs = mutation.get_inputs(["form"])

    result = []
    for field_name in field_names or _get_field_names(
        scalar_field_specs, form_field_specs
    ):
        if "." in field_name:
            for form_field_spec in form_field_specs:
                for scalar_field_spec in _form_fields(form_field_spec):
                    form_field_name = f"{form_field_spec.name}.{scalar_field_spec.name}"
                    if field_name == form_field_name:
                        result.append((field_name, scalar_field_spec))
                        break
        else:
            for scalar_field_spec in scalar_field_specs:
                if field_name == scalar_field_spec.name:
                    result.append((field_name, scalar_field_spec))
                    break

    return result


def _form_fields(form_field_spec):
    return [
        x
        for x in form_field_spec.target_type_spec.get_field_specs()
        if "client" in x.has_model
    ]


def _get_field_names(scalar_field_specs, form_field_specs):
    result = [x.name for x in scalar_field_specs]
    for form_field_spec in form_field_specs:
        result.extend(
            [f"{form_field_spec.name}.{x.name}" for x in _form_fields(form_field_spec)]
        )
    return result
