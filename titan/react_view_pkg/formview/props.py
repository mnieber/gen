import ramda as R
from moonleap import upper0
from moonleap.resources.type_spec_store import type_spec_store
from titan.react_pkg.reactapp.resources import find_module_that_provides_item_list


class Sections:
    def __init__(self, res):
        self.res = res
        self.item_name = res.item_name
        self.form_type_spec_name = upper0(self.item_name) + "Form"
        self.form_type_spec = type_spec_store().get(self.form_type_spec_name)
        self.form_field_specs = [
            x for x in self.form_type_spec.field_specs if x.name != "id"
        ]

        self.react_app = res.module.react_app
        self.react_module = find_module_that_provides_item_list(
            self.react_app, self.item_name
        )

        self.graphql_api = self.react_app.api_module.graphql_api
        self.mutation = R.head(
            self.graphql_api.mutations_that_post_item(self.item_name)
        )
        self.postmethod = self.mutation.name
