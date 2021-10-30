from moonleap import named
from titan.react_pkg.component import Component
from titan.react_pkg.pkg.get_chain import (
    TakeHighlightedElmFromState,
    TakeItemFromQuery,
    TakeItemFromState,
    TakeItemListFromQuery,
    TakeItemListFromState,
)
from titan.react_state_pkg.state.resources import State
from titan.react_view_pkg.router.resources import concat_router_configs


def _create_named_item(obj):
    result = named(Component)()
    result.typ = obj
    result.name = ""
    return result


def create_router_configs_from_chain(chain):
    result = []
    for i in range(len(chain)):
        elm = chain[i]
        if isinstance(elm, (TakeItemListFromQuery, TakeItemFromQuery)):
            load_item_effect = elm.side_effects[0].subj.react_load_effect
            result = concat_router_configs(
                result,
                load_item_effect.create_router_configs(
                    named_component=_create_named_item(load_item_effect)
                ),
            )
        elif isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
        ):
            state_provider = elm.subj.state_provider
            router_configs = state_provider.create_router_configs(
                named_component=_create_named_item(state_provider)
            )
            if isinstance(elm, TakeHighlightedElmFromState):
                select_item_effect = elm.side_effects[0].subj.react_select_effect
                router_configs[-1].side_effects.extend(
                    select_item_effect.create_router_configs(
                        named_component=_create_named_item(select_item_effect)
                    )
                )
            result = concat_router_configs(
                result,
                router_configs,
            )
        elif isinstance(elm, (TakeHighlightedElmFromState,)):
            state_provider = elm.subj.state_provider
            result = concat_router_configs(
                result,
                state_provider.create_router_configs(
                    named_component=_create_named_item(state_provider)
                ),
            )

    return result
