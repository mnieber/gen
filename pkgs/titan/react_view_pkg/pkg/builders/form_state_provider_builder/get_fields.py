import typing as T

from typespec.api_spec import ApiSpec


def get_fields(mutation: ApiSpec, fields: T.Optional[list[str]]):
    scalar_field_specs = [x for x in mutation.get_inputs() if x.field_type != "form"]
    result = []
    result.extend([(x.name, x) for x in scalar_field_specs])
    for form_field_spec in mutation.get_inputs(["form"]):
        result.extend(
            [
                (f"{form_field_spec.name}.{x.name}", x)
                for x in _form_fields(form_field_spec)
                if not (x.field_type == "uuid" and not x.target)
            ]
        )
    return result


def _form_fields(form_field_spec):
    return [
        x
        for x in form_field_spec.target_type_spec.get_field_specs()
        if "client" in x.has_model
    ]
