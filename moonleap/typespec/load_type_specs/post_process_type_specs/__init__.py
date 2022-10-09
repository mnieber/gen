from . import (
    add_missing_fk,
    add_missing_parent_child,
    add_sortpos_field,
    assert_no_duplicate_fields,
    maybe_make_fks_optional,
    set_display_by_value,
    set_is_reverse_of_related_set,
)


def post_process_type_specs(type_spec_store):
    for type_spec in type_spec_store.type_specs():
        assert_no_duplicate_fields.assert_no_duplicate_fields(type_spec)

    for type_spec in type_spec_store.type_specs():
        set_display_by_value.set_display_by_value(type_spec)

    for type_spec in type_spec_store.type_specs():
        add_sortpos_field.add_sortpos_field(type_spec)

    for type_spec in type_spec_store.type_specs():
        set_is_reverse_of_related_set.set_is_reverse_of_related_set(
            type_spec_store, type_spec
        )

    for type_spec in type_spec_store.type_specs():
        add_missing_fk.add_missing_fk(type_spec_store, type_spec)

    for type_spec in type_spec_store.type_specs():
        add_missing_parent_child.add_missing_parent_child(type_spec_store, type_spec)

    for type_spec in type_spec_store.type_specs():
        maybe_make_fks_optional.maybe_make_fks_optional(type_spec_store, type_spec)
