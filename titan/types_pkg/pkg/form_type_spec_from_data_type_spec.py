from copy import deepcopy
from dataclasses import replace

import ramda as R
from titan.typespec.type_spec import TypeSpec


def form_type_spec_from_data_type_spec(data_type_spec, form_type_name):
    def _convert(field_spec):
        new_field_spec = deepcopy(field_spec)

        changes = {}
        if field_spec.field_type in ("fk",):
            changes = dict(
                key=field_spec.key + "Id",
                field_type="uuid",
                target=field_spec.target,
            )

        return replace(new_field_spec, **changes)

    form_type_spec = TypeSpec(
        type_name=form_type_name,
        base_type_name=None,
        is_form=True,
        is_entity=False,
        is_sorted=False,
        only_api=False,
        field_specs=R.pipe(
            R.always(data_type_spec.field_specs),
            R.filter(lambda x: x.field_type != "relatedSet"),
            R.map(_convert),
        )(None),
    )
    return form_type_spec
