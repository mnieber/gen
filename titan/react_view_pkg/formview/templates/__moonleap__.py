import ramda as R


def get_helpers(_):
    class Helpers:
        form_view = _.component
        type_spec = form_view.item_posted.item_type.form_type.type_spec
        field_specs = [x for x in type_spec.field_specs if x.name != "id"]
        fk_field_specs = [x for x in type_spec.get_field_specs(["uuid"]) if x.target]
        mutation = R.head(form_view.item_posted.poster_mutations)

    return Helpers()
