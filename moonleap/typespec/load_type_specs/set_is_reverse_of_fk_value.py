from moonleap.typespec.field_spec import FkFieldSpec
from moonleap.typespec.load_type_specs.get_target_type_spec import get_target_type_spec


def set_is_reverse_of_fk_value(
    type_spec_store, type_spec, fk_field_spec: FkFieldSpec, parent_node
):
    assert fk_field_spec.field_type == "fk"

    # If Team.memberSet targets Member, and Member.team targets Team, then we need
    # to set the related name of Member.team.
    target_type_spec = get_target_type_spec(type_spec_store, fk_field_spec)
    if target_type_spec and target_type_spec.type_name == parent_node["__type_name__"]:
        for target_field_spec in target_type_spec.get_field_specs(["relatedSet"]):
            if target_field_spec.name in parent_node["__field_names__"]:
                if target_field_spec.target == type_spec.type_name:
                    target_field_spec.is_reverse_of_related_set = target_field_spec
                    break
