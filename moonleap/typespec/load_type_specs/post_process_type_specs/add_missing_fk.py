from moonleap.typespec.field_spec import FkFieldSpec
from moonleap.typespec.load_type_specs.get_target_type_spec import get_target_type_spec
from moonleap.utils.case import l0


def add_missing_fk(type_spec_store, type_spec):
    for fk_field_spec in type_spec.get_field_specs(["fk", "relatedSet"]):
        # Case 1: Team.sloganSet targets Slogan, and Slogan has no fk to Team yet
        target_type_spec = get_target_type_spec(type_spec_store, fk_field_spec)

        if target_type_spec and fk_field_spec.field_type == "relatedSet":
            has_fk = False
            for target_field_spec in target_type_spec.get_field_specs(["fk"]):
                if target_field_spec.target == type_spec.type_name:
                    has_fk = True
                    break

            if not has_fk:
                reverse_fk = FkFieldSpec(
                    name=l0(type_spec.type_name),
                    target=type_spec.type_name,
                    field_type="fk",
                )

                reverse_fk.is_reverse_of_related_set = fk_field_spec
                target_type_spec.field_specs.append(reverse_fk)

        if fk_field_spec.through and fk_field_spec.through != "+":
            through_type_spec = type_spec_store.get(fk_field_spec.through)

            # Case 2: add TeamMember.team
            has_fk = False
            for through_field_spec in through_type_spec.get_field_specs(["fk"]):
                if through_field_spec.target == type_spec.type_name:
                    has_fk = True
                    break

            if not has_fk:
                through_type_spec.field_specs.append(
                    FkFieldSpec(
                        name=l0(type_spec.type_name),
                        field_type="fk",
                        target=type_spec.type_name,
                    )
                )

            # Case 3: add TeamMember.member
            has_fk = False
            for through_field_spec in through_type_spec.get_field_specs(["fk"]):
                if through_field_spec.target == fk_field_spec.target:
                    has_fk = True
                    break

            if not has_fk:
                through_type_spec.field_specs.append(
                    FkFieldSpec(
                        name=l0(fk_field_spec.target),
                        field_type="fk",
                        target=fk_field_spec.target,
                    )
                )

            # Case 4: Team has a relatedSet to TeamMember
            has_fk = False
            for field_spec in type_spec.get_field_specs(["relatedSet"]):
                if field_spec.target == fk_field_spec.through:
                    has_fk = True
                    break

            if not has_fk:
                default_name = l0(fk_field_spec.through) + "Set"
                type_spec.field_specs.append(
                    FkFieldSpec(
                        name=fk_field_spec.through_as or default_name,
                        field_type="relatedSet",
                        target=fk_field_spec.through,
                    )
                )
                type_spec_store.register_parent_child(
                    type_spec.type_name,
                    fk_field_spec.through,
                    fk_field_spec.is_parent_of_through,
                )
