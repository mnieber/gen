import os

from moonleap.typespec.get_member_field_spec import get_member_field_spec
from moonleap.utils.case import l0
from moonleap.utils.inflect import plural
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.pkg.get_chain import (
    ExtractItemFromItem,
    ExtractItemListFromItem,
    TakeHighlightedElmFromState,
    TakeItemFromState,
    TakeItemFromStore,
    TakeItemListFromState,
    TakeItemListFromStore,
    get_chain_to,
)
from titan.react_pkg.pkg.ts_var import (
    ts_type,
    ts_type_import_path,
    ts_var,
    ts_var_by_id,
)
from titan.react_view_pkg.pkg.create_component_router_config import (
    create_component_router_config,
)


def create_router_configs(self):
    result = []

    if self.state:
        router_config = create_component_router_config(
            self, wraps=True, url=get_component_base_url(self, "")
        )
        result.append(router_config)

    return result


def _get_default_input_props(chain):
    result = []
    for elm in chain:
        if isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
        ):
            result += [elm.obj]
    return result


def _get_input_stores(chain):
    result = []
    for elm in chain:
        if isinstance(elm, (TakeItemListFromStore, TakeItemFromStore)):
            result += [elm.subj]
        if isinstance(elm, (ExtractItemFromItem, ExtractItemListFromItem)):
            result += [elm.obj.provider_react_store]
    return result


def _start_pos(chain):
    for pos in reversed(range(len(chain))):
        elm = chain[pos]
        if isinstance(
            elm,
            (
                TakeItemListFromState,
                TakeItemFromState,
                TakeHighlightedElmFromState,
                TakeItemListFromStore,
                TakeItemFromStore,
            ),
        ):
            return pos
    return 0


def _expression(chain):
    result = ""
    for elm in chain:
        if isinstance(elm, (TakeItemListFromStore)):
            result = (
                f"R.values({ts_var(elm.subj)}.{ts_var_by_id(elm.obj.item)})" + result
            )
        elif isinstance(elm, (TakeItemFromStore)):
            result = f"{ts_var(elm.subj)}.{ts_var(elm.obj)}" + result
        elif isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
        ):
            result = f"props.{ts_var(elm.obj)}?" + result
        elif isinstance(elm, (ExtractItemFromItem)):
            store = ts_var(elm.obj.item_list.provider_react_store)
            var_by_id = ts_var_by_id(elm.obj)
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj
            ).name
            result = f"{store}.{var_by_id}[{result}.{member}]"
        elif isinstance(elm, (ExtractItemListFromItem)):
            store = ts_var(elm.obj.provider_react_store)
            var_by_id = ts_var_by_id(elm.obj.item)
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj
            ).name
            result = (
                f"R.reject(R.isNil)"
                + f"(lookUp({result}.{member} ?? [], {store}.{var_by_id}))"
            )
    return result


def get_context(state_provider):
    _ = lambda: None
    _.state = state_provider.state

    _.chains = []
    for target in list(_.state.items_provided) + list(_.state.item_lists_provided):
        chain = get_chain_to(target, _.state)
        _.chains.append(chain[_start_pos(chain) : len(chain)])

    _.default_input_props = []
    for chain in _.chains:
        for default_input_prop in _get_default_input_props(chain):
            if default_input_prop not in _.default_input_props:
                _.default_input_props.append(default_input_prop)

    _.stores = []
    for chain in _.chains:
        for store in _get_input_stores(chain):
            if store not in _.stores:
                _.stores.append(store)

    class Sections:
        def declare_default_input_props(self):
            result = [f"{ts_var(x)}: {ts_type(x)}," for x in _.default_input_props]
            return "; ".join(result)

        def input_stores(self):
            result = [ts_var(x) for x in _.stores]
            return ", ".join(result)

        def default_prop_type_imports(self):
            result = [
                f"import {{ {ts_type(x)} }} from '{ts_type_import_path(x)}';"
                for x in _.default_input_props
            ]
            return os.linesep.join(result)

        def get_state_input_values(self):
            result = []
            for chain in _.chains:
                provided = chain[-1].obj
                expression = _expression(chain)
                result.append(f"{ts_var(provided)}: {expression},")
            return os.linesep.join(result)

        def set_state_input_values(self):
            result = []
            tab = " " * 8
            for chain in _.chains:
                provided = chain[-1].obj
                result.append(
                    f"{tab}state.inputs.{ts_var(provided)} = inputs.{ts_var(provided)};"
                )
            return os.linesep.join(result)

        def default_props(self):
            result = ""

            if _.state:
                result = f"      {_.state.name}State: () => state,\n"
                store_by_item_name = _.state.store_by_item_name
                for item_name, bvrs in _.state.bvrs_by_item_name.items():
                    store = store_by_item_name.get(item_name)
                    items_name = plural(item_name)

                    result += f"      {items_name}: () => state.outputs.{items_name}Display,\n"
                    result += f"      {items_name}ResUrl: () => {l0(store.name)}.resUrls().{item_name}ById,\n"  # noqa: E501

                    for bvr in bvrs:
                        result += bvr.sections.default_props(store)
            return result

    return dict(sections=Sections())
