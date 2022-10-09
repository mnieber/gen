from moonleap.typespec.field_spec import FieldSpec


def add_sortpos_field(type_spec):
    if type_spec.is_sorted and not type_spec.get_field_spec("sortPos"):
        type_spec.field_specs.append(
            FieldSpec(key="sortPos", field_type="int", default_value=0)
        )
