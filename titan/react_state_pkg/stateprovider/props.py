import os

from moonleap import u0
from moonleap.typespec.get_member_field_spec import get_member_field_spec
from moonleap.utils.case import l0
from moonleap.utils.inflect import plural
from titan.api_pkg.pkg.ml_name import ml_type_spec_from_item_name
from titan.api_pkg.typeregistry import TypeRegistry
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
from titan.react_pkg.pkg.ml_get import ml_graphql_api, ml_react_app
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


def _get_default_input_props(chain):
    result = []
    for elm in chain:
        if isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
        ):
            result += [elm.obj]
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


def get_items_selected_from_url(state_provider):
    graphql_api = ml_graphql_api(ml_react_app(state_provider))
    type_reg = TypeRegistry(graphql_api)
    result = []
    if state_provider.state:
        for item_name, bvrs in state_provider.state.bvrs_by_item_name.items():
            if [x for x in bvrs if x.name == "selection"]:
                item = type_reg.get_item_by_name(item_name)
                type_spec = ml_type_spec_from_item_name(item_name)
                if type_spec.select_item_by:
                    result.append(item)
    return result


def get_context(state_provider):
    _ = lambda: None
    _.state = state_provider.state
    _.selected_items = get_items_selected_from_url(state_provider)

    _.chains = []
    for target in list(_.state.items_provided) + list(_.state.item_lists_provided):
        chain = get_chain_to(target, _.state)
        _.chains.append(chain[_start_pos(chain) : len(chain)])

    _.default_input_props = []
    for chain in _.chains:
        for default_input_prop in _get_default_input_props(chain):
            if default_input_prop not in _.default_input_props:
                _.default_input_props.append(default_input_prop)

    _.query_names = set()
    for chain in _.chains:
        elm = chain[-1]
        if isinstance(elm, TakeItemListFromQuery):
            _.query_names.add(elm.subj.name)

    class Sections:
        def declare_default_input_props(self):
            result = [f"{ts_var(x)}: {ts_type(x)}," for x in _.default_input_props]
            return "; ".join(result)

        def default_prop_type_imports(self):
            result = [
                f"import {{ {ts_type(x)} }} from '{ts_type_import_path(x)}';"
                for x in _.default_input_props
            ]
            return os.linesep.join(result)

        def query_imports(self):
            return os.linesep.join(
                [
                    f"import {{ use{u0(x)} }} from 'src/api/queries';"
                    for x in _.query_names
                ]
            )

        def get_queries(self):
            return os.linesep.join(
                [f"    const {x} = use{u0(x)}()" for x in _.query_names]
            )

        def get_state_input_values(self):
            result = []
            for chain in _.chains:
                provided = ts_var(chain[-1].obj)
                value, value_rs = _expression(chain)
                result.append(f"{provided}: {value},")
                if value_rs:
                    result.append(f"{provided}RS: {value_rs},")
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
                state_by_item_name = _.state.state_by_item_name
                for item_name, bvrs in _.state.bvrs_by_item_name.items():
                    state = state_by_item_name.get(item_name)
                    items_name = plural(item_name)

                    result += f"      {items_name}: () => state.outputs.{items_name}Display,\n"
                    result += f"      {items_name}RS: () => state.inputs.{items_name}RS,\n"  # noqa: E501

                    for bvr in bvrs:
                        result += bvr.sections.default_props(state)
            return result

    return dict(sections=Sections(), _=_)
