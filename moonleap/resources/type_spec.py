import typing as T
from dataclasses import dataclass, replace

import ramda as R
from moonleap.resources.field_spec import FieldSpec, type_name_to_item_name
from moonleap.utils.case import camel_to_snake, lower0


@dataclass
class TypeSpec:
    type_name: str
    field_specs: T.List[FieldSpec]


def add_related_set_field_to_type_spec(type_spec, field_spec, fk_type_spec):
    name = lower0(type_spec.type_name + "Set")
    if [x for x in fk_type_spec.field_specs if x.name == name]:
        raise Exception("Field spec with name {name} already exists")

    fk_type_spec.field_specs.append(
        FieldSpec(
            name=name,
            name_snake=camel_to_snake(name),
            required=False,
            private=field_spec.private,
            field_type="related_set",
            field_type_attrs=dict(
                target=type_spec.type_name,
                item_name=type_name_to_item_name(type_spec.type_name),
            ),
        )
    )


def form_type_spec_from_data_type_spec(data_type_spec):
    def _convert(field_spec):
        changes = {}
        if field_spec.field_type in ("fk",):
            changes = dict(
                field_type="uuid",
                field_type_attrs={},
            )

        return replace(field_spec, **changes)

    return TypeSpec(
        type_name=data_type_spec.type_name + "Form",
        field_specs=R.pipe(
            R.always(data_type_spec.field_specs),
            R.filter(lambda x: x.field_type != "related_set"),
            R.map(_convert),
        )(None),
    )
