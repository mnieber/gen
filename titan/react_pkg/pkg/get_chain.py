import typing as T
from dataclasses import dataclass, field

from moonleap import Resource, Term
from moonleap.resource.rel import Rel
from moonleap.utils.join import join
from moonleap.verbs import uses
from titan.api_pkg.item.resources import Item
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name


def get_select_item_effect_term(item):
    type_spec = ml_type_spec_from_item_name(item.item_name)
    name_postfix = join("-by-", "-and-".join(type_spec.select_item_by))
    return Term(f"select-{item.meta.term.data}{name_postfix}", "select-item-effect")


@dataclass
class ChainElm:
    obj: T.Optional[Resource] = None
    subj: T.Optional[Resource] = None
    side_effects: T.List[Rel] = field(default_factory=list)


class TakeItemListFromState(ChainElm):
    pass


class TakeItemFromState(ChainElm):
    @staticmethod
    def get_side_effects(item):
        return []


class TakeItemListFromQuery(ChainElm):
    @staticmethod
    def get_side_effects(item_list):
        return []


class TakeItemFromQuery(ChainElm):
    @staticmethod
    def get_side_effects(item):
        return []


class ExtractItemFromItem(ChainElm):
    pass


class ExtractItemListFromItem(ChainElm):
    pass


@dataclass
class TakeHighlightedElmFromState(ChainElm):
    item_list: T.Any = None

    @staticmethod
    def get_side_effects(item_list):
        return [Rel(item_list, uses, get_select_item_effect_term(item_list.item))]


class StoreItemInState(ChainElm):
    pass


class StoreItemListInState(ChainElm):
    pass


def get_chain_to(target, next_target=None, stop_list=None):
    from titan.api_pkg.itemlist.resources import ItemList
    from titan.react_state_pkg.state.resources import State

    stop_list = stop_list or []
    consider_states = True
    consider_queries = isinstance(next_target, State)

    if isinstance(target, ItemList):
        item_list = target

        # If there is a state that provides this item_list, then check if there
        # is a chain that leads to this state
        for state in item_list.provider_react_states if consider_states else []:
            if state is next_target:
                continue

            stop_elm = (state, item_list)
            if stop_elm in stop_list:
                continue
            chain = get_chain_to(state, item_list, stop_list + [stop_elm])
            if chain:
                elm = TakeItemListFromState(
                    subj=state,
                    obj=item_list,
                )

                return chain + [elm]

        # If there is a query that provides this item_list, then start the chain
        # with this query
        for query in item_list.provider_queries if consider_queries else []:
            return [
                TakeItemListFromQuery(
                    subj=query,
                    side_effects=TakeItemListFromQuery.get_side_effects(item_list),
                    obj=item_list,
                )
            ]

        # If some item provides this item_list, then check if there
        # is a chain that leads to this other item
        for provider_item in item_list.provider_items:
            stop_elm = (provider_item, item_list)
            if stop_elm in stop_list:
                continue
            chain = get_chain_to(provider_item, next_target, stop_list + [stop_elm])
            if chain:
                elm = ExtractItemListFromItem(subj=provider_item, obj=item_list)
                return chain + [elm]

    elif isinstance(target, Item):
        item = target

        # If there is a state that provides this item, then check if there
        # is a chain that leads to this state
        for state in item.provider_react_states if consider_states else []:
            if state is next_target:
                continue

            stop_elm = (state, item)
            if stop_elm in stop_list:
                continue
            chain = get_chain_to(state, item, stop_list + [stop_elm])
            if chain:
                elm = TakeItemFromState(
                    subj=state,
                    side_effects=TakeItemFromState.get_side_effects(item),
                    obj=item,
                )
                return chain + [elm]

        # Find a state that provides this item as a selection in a list
        item_list = item.item_list
        if item_list:
            for state in item_list.provider_react_states if consider_states else []:
                if item_list.item_name in [x.item_name for x in state.selections]:
                    stop_elm = (state, item)
                    if stop_elm in stop_list:
                        continue
                    chain = get_chain_to(state, item_list, stop_list + [stop_elm])
                    if chain:
                        elm = TakeHighlightedElmFromState(
                            subj=state,
                            item_list=item_list,
                            side_effects=TakeHighlightedElmFromState.get_side_effects(
                                item_list
                            ),
                            obj=item,
                        )
                        return chain + [elm]

        # If there is a query that provides this item_list, then start the chain
        # with this query
        for query in item.provider_queries if consider_queries else []:
            return [
                TakeItemFromQuery(
                    subj=query,
                    side_effects=TakeItemFromQuery.get_side_effects(item),
                    obj=item,
                )
            ]

        # If some other item provides this item, then check if there
        # is a chain that leads to this other item
        for provider_item in item.provider_items:
            stop_elm = (provider_item, item)
            if stop_elm in stop_list:
                continue
            chain = get_chain_to(provider_item, next_target, stop_list + [stop_elm])
            if chain:
                elm = ExtractItemFromItem(
                    subj=provider_item,
                    obj=item,
                )

                return chain + [elm]

    elif isinstance(target, State):
        state = target

        if isinstance(next_target, ItemList):
            item_list = next_target
            chain = get_chain_to(item_list, state, stop_list)
            if chain:
                return chain + [StoreItemListInState(subj=item_list, obj=state)]

        if isinstance(next_target, Item):
            item = next_target
            chain = get_chain_to(item, state, stop_list)
            if chain:
                return chain + [StoreItemInState(subj=item, obj=state)]

    return []
