from moonleap.typespec.field_spec import FieldSpec


def add_sortpos_field(type_spec):
    if type_spec.is_sorted and not type_spec.get_field_spec("sortPos", False):
        type_spec.field_specs.append(
            FieldSpec(name="sortPos", field_type="int", default_value=0)
        )
