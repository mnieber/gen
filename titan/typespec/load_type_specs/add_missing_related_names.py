def add_missing_related_names(type_reg):
    for type_spec in type_reg.type_specs():
        for fk_field_spec in type_spec.get_field_specs(["fk"]):
            # Check if the target typespec has a relatedSet that points back
            # to this fk_field_spec (note that we need the related_name of the relatedSet
            # to check this). In that case, update the related_name of fk_field_spec.
            target_type_spec = type_reg.get(fk_field_spec.target)
            assert target_type_spec

            for related_set_field_spec in target_type_spec.get_field_specs(
                ["relatedSet"]
            ):
                if related_set_field_spec.target == type_spec.type_name:
                    if related_set_field_spec.related_name == fk_field_spec.key:
                        fk_field_spec.related_name = related_set_field_spec.key
