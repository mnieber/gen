def get_helpers(_):
    class Helpers:
        form_view = _.component
        mutation = form_view.mutation
        field_specs = [x for x in mutation.gql_spec.get_inputs() if x.name != "id"]
        fk_field_specs = [x for x in mutation.gql_spec.get_inputs(["uuid"]) if x.target]

    return Helpers()
