import ramda as R
from moonleap.resources.data_type_spec_store import data_type_spec_store
from titan.react_module_pkg.form.resources import Form
from titan.react_module_pkg.loaditemeffect.resources import (
    LoadItemEffect,
    shorten_route_params,
)


def schema_item_names(self):
    return R.uniq(
        [x.item_name for x in self.items_loaded]
        + [x.item_name for x in self.item_lists_loaded]
    )


class Sections:
    def __init__(self, res):
        self.res = res

    def load_item_effect(self, load_item_effect: LoadItemEffect):
        short_params = shorten_route_params(
            load_item_effect.route_params, load_item_effect.item_name
        )
        return {
            "params": ", ".join([f"{x}: string" for x in short_params]),
            "graphql_params": ",\n".join(
                [f"{' ' * 8}${x}: String" for x in short_params]
            ),
            "graphql_params_inner": ",\n".join(
                [f"{' ' * 10}{x}: ${x}" for x in short_params]
            ),
            "vars": ", ".join(short_params),
        }

    def post_form(self, form: Form):
        spec = data_type_spec_store.get_spec(form.item_name)

        return {
            "params": ", ".join([f"{x.name}: {x.field_type}" for x in spec.fields]),
            "graphql_params": "",
            "graphql_params_inner": "",
            "vars": "",
        }

    def item_fields(self, item_name):
        spec = data_type_spec_store.get_spec(item_name)
        return "\n".join([f"          {x.name}," for x in spec.fields if not x.private])
