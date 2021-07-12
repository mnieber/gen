import ramda as R
from moonleap_react_module.loaditemeffect.resources import (
    LoadItemEffect,
    shorten_route_params,
)


def item_names(self):
    return R.uniq(
        [x.item_name for x in self.items] + [x.item_name for x in self.item_lists]
    )


def params(self, load_item_effect: LoadItemEffect):
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
