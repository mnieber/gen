import ramda as R
from moonleap.resources.data_type_spec_store import data_type_spec_store
from moonleap_react_module.form.resources import Form
from moonleap_react_module.loaditemeffect.resources import (
    LoadItemEffect,
    shorten_route_params,
)


def schema_item_names(self):
    return R.uniq(
        [x.item_name for x in self.items_loaded]
        + [x.item_name for x in self.item_lists_loaded]
    )


def p_section_load_item_effect(self, load_item_effect: LoadItemEffect):
    short_params = shorten_route_params(
        load_item_effect.route_params, load_item_effect.item_name
    )
    return {
        "params": ", ".join([f"{x}: string" for x in short_params]),
        "graphql_params": ",\n".join([f"{' ' * 8}${x}: String" for x in short_params]),
        "graphql_params_inner": ",\n".join(
            [f"{' ' * 10}{x}: ${x}" for x in short_params]
        ),
        "vars": ", ".join(short_params),
    }


def p_section_post_form(self, form: Form):
    spec = data_type_spec_store.get_spec(form.item_name)

    return {
        "params": ", ".join([f"{x.name_camel}: {x.field_type}" for x in spec.fields]),
        "graphql_params": "",
        "graphql_params_inner": "",
        "vars": "",
    }


def p_section_item_fields(self, item_name):
    spec = data_type_spec_store.get_spec(item_name)
    return "\n".join(
        [f"          {x.name_camel}," for x in spec.fields if not x.private]
    )
