import ramda as R
from moonleap import u0
from moonleap.resources.type_spec_store import type_spec_store
from titan.react_pkg.reactapp.resources import find_module_that_provides_item_list


def get_context(res):
    _ = lambda: None
    _.item_name = res.item_name
    _.form_type_spec_name = u0(_.item_name) + "Form"
    _.form_type_spec = type_spec_store().get(_.form_type_spec_name)
    _.form_field_specs = [x for x in _.form_type_spec.field_specs if x.name != "id"]

    _.react_app = res.module.react_app
    _.react_module = find_module_that_provides_item_list(_.react_app, _.item_name)

    _.graphql_api = _.react_app.api_module.graphql_api
    _.mutation = R.head(_.graphql_api.mutations_that_post_item(_.item_name))
    _.postmethod = _.mutation.name

    class Sections:
        pass

    return dict(sections=Sections(), _=_)
