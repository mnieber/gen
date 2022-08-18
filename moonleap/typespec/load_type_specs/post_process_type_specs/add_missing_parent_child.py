def add_missing_parent_child(type_spec_store, type_spec):
    for fk_field_spec in type_spec.get_field_specs(["fk", "relatedSet"]):
        # If Team.member is an fk that targets Member but not as the
        # reverse of a relatedSet, then add a parent/child relation.
        if fk_field_spec.field_type == "relatedSet" or (
            fk_field_spec.field_type == "fk"
            and not fk_field_spec.is_reverse_of_related_set
        ):
            type_spec_store.register_parent_child(
                type_spec.type_name,
                fk_field_spec.target,
                fk_field_spec.is_parent_of_target,
            )
