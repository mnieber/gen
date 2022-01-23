import os

from moonleap.typespec.get_member_field_spec import get_member_field_spec
from moonleap.utils.inflect import plural
from titan.react_pkg.component.resources import get_component_base_url
from titan.react_pkg.pkg.get_chain import (
    ExtractItemFromItem,
    ExtractItemListFromItem,
    TakeHighlightedElmFromState,
    TakeItemFromState,
    TakeItemListFromQuery,
    TakeItemListFromState,
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


def create_router_configs(self, named_component):
    result = []

    if self.state:
        router_config = create_component_router_config(
            self,
            named_component=named_component,
            wraps=True,
            url=get_component_base_url(self, ""),
        )
        result.append(router_config)

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
            ),
        ):
            return pos
    return 0


def _get_default_input_props(chain):
    result = []
    for elm in chain:
        if isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
        ):
            result += [elm.obj]
    return result


def _expression(chain):
    result = ""
    result_rs = None
    for elm in chain:
        if isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
        ):
            result = f"props.{ts_var(elm.obj)}?" + result
        if isinstance(elm, (TakeItemListFromQuery,)):
            query_name = elm.subj.name
            items_name = plural(elm.obj.item_name)
            result = f"R.values({query_name}.data?.{items_name} ?? {{}})"
            result_rs = f"{query_name}.status"
        elif isinstance(elm, (ExtractItemFromItem)):
            state = ts_var(elm.obj.item_list.provider_react_state)
            var_by_id = ts_var_by_id(elm.obj)
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj
            ).name
            result = f"{state}.{var_by_id}[{result}.{member}]"
        elif isinstance(elm, (ExtractItemListFromItem)):
            state = ts_var(elm.obj.provider_react_state)
            var_by_id = ts_var_by_id(elm.obj.item)
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj
            ).name
            result = (
                f"R.reject(R.isNil)"
                + f"(lookUp({result}.{member} ?? [], {state}.{var_by_id}))"
            )
    return result, result_rs


def get_context(state_provider):
    _ = lambda: None
    _.state = state_provider.state

    _.chains = []
    _.short_chains = []
    for target in list(_.state.items_provided) + list(_.state.item_lists_provided):
        chain = get_chain_to(target, _.state)
        _.chains.append(chain)
        _.short_chains.append(chain[_start_pos(chain) : len(chain)])

    _.default_input_props = []
    for chain in _.short_chains:
        for default_input_prop in _get_default_input_props(chain):
            if default_input_prop not in _.default_input_props:
                _.default_input_props.append(default_input_prop)

    _.query_names = set()
    for chain in _.chains:
        _.query_names.add(chain[0].subj.name)

    _.ts_type = ts_type
    _.ts_var = ts_var
    _.ts_type_import_path = ts_type_import_path

    class Sections:
        def get_state_input_values(self):
            result = []
            for chain in _.short_chains:
                provided = ts_var(chain[-1].obj)
                value, value_rs = _expression(chain)
                result.append(f"{provided}: {value},")
                if value_rs:
                    result.append(f"{provided}RS: {value_rs},")
            return os.linesep.join(result)

        def set_state_input_values(self):
            result = []
            tab = " " * 8
            for chain in _.short_chains:
                provided = chain[-1].obj
                result.append(
                    f"{tab}state.inputs.{ts_var(provided)} = inputs.{ts_var(provided)};"
                )
            return os.linesep.join(result)

        def default_props(self):
            result = ""

            if _.state:
                result = f"      {_.state.name}State: () => state,\n"
                for item_name, bvrs in _.state.bvrs_by_item_name.items():
                    items_name = plural(item_name)

                    result += f"      {items_name}: () => state.outputs.{items_name}Display,\n"
                    result += f"      {items_name}RS: () => state.inputs.{items_name}RS,\n"  # noqa: E501

                    for bvr in bvrs:
                        result += bvr.sections.default_props(_.state)
            return result

    return dict(sections=Sections(), _=_)
