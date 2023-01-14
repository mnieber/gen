import typing as T
from dataclasses import dataclass

from titan.api_pkg.mutation import Mutation
from titan.api_pkg.pipeline.resources import PropsSource
from titan.api_pkg.query import Query
from titan.react_view_pkg.behavior import Behavior
from titan.types_pkg.item import Item
from titan.types_pkg.itemlist import ItemList
from titan.types_pkg.pkg.get_member_field_spec import get_member_field_spec

from moonleap import Resource, named
from moonleap.utils.fp import aperture


@dataclass
class PipelineElement:
    obj: T.Optional[Resource] = None
    subj: T.Optional[Resource] = None


class TakeItemListFromStateProvider(PipelineElement):
    pass


class TakeItemFromStateProvider(PipelineElement):
    pass


class TakeBvrFromProps(PipelineElement):
    pass


class TakeItemListFromProps(PipelineElement):
    pass


class TakeItemFromProps(PipelineElement):
    pass


class TakeItemListFromQuery(PipelineElement):
    pass


class TakeItemFromQuery(PipelineElement):
    pass


class ExtractItemFromItem(PipelineElement):
    pass


class ExtractItemListFromItem(PipelineElement):
    pass


@dataclass
class TakeHighlightedElmFromStateProvider(PipelineElement):
    pass


def _get_elements(self):
    from titan.react_view_pkg.stateprovider.resources import StateProvider

    if hasattr(self, "_elements"):
        return self._elements

    result = []
    resources = [self.source] + list(self.resources)
    for res, next_res in aperture(2, resources):
        if isinstance(res, (Query, Mutation)):
            query = res
            if isinstance(next_res, named(Item)):
                named_item = next_res
                result.append(
                    TakeItemFromQuery(
                        subj=query,
                        obj=named_item,
                    )
                )
            elif isinstance(next_res, named(ItemList)):
                named_item_list = next_res
                result.append(
                    TakeItemListFromQuery(
                        subj=query,
                        obj=named_item_list,
                    )
                )
            else:
                raise Exception(f"Unexpected resource sequence: {res}, {next_res}")

        elif isinstance(res, StateProvider):
            state_provider = res
            if isinstance(next_res, named(Item)):
                found = False
                named_item = next_res
                for provided_named_item in state_provider.named_items_provided:
                    if _match_named_item(named_item, provided_named_item):
                        found = True
                        result.append(
                            TakeItemFromStateProvider(
                                subj=state_provider,
                                obj=named_item,
                            )
                        )

                if not found and state_provider.state:
                    for c in state_provider.state.containers:
                        highlight = c.get_bvr("highlight")
                        if (
                            highlight
                            and highlight.item_name == named_item.typ.item_name
                        ):
                            found = True
                            result.append(
                                TakeHighlightedElmFromStateProvider(
                                    subj=state_provider,
                                    obj=named_item,
                                )
                            )

                if not found:
                    raise Exception(
                        f"Cannot take {next_res} from state provider {state_provider}"
                    )

            elif isinstance(next_res, named(ItemList)):
                named_item_list = next_res
                result.append(
                    TakeItemListFromStateProvider(
                        subj=state_provider.state,
                        obj=named_item_list,
                    )
                )
            else:
                raise Exception(f"Unexpected resource sequence: {res}, {next_res}")

        elif isinstance(res, named(Item)):
            item = res.typ
            if isinstance(next_res, named(Item)):
                named_item = next_res
                result.append(
                    ExtractItemFromItem(
                        subj=item,
                        obj=named_item,
                    )
                )
            elif isinstance(next_res, named(ItemList)):
                named_item_list = next_res
                result.append(
                    ExtractItemListFromItem(
                        subj=item,
                        obj=named_item_list,
                    )
                )
            else:
                raise Exception(f"Unexpected resource sequence: {res}, {next_res}")
        elif isinstance(res, named(ItemList)):
            raise NotImplementedError(f"{res}")
        elif isinstance(res, PropsSource):
            if isinstance(next_res, named(Item)):
                named_item = next_res
                result.append(
                    TakeItemFromProps(
                        subj=res,
                        obj=named_item,
                    )
                )
            elif isinstance(next_res, named(ItemList)):
                named_item_list = next_res
                result.append(
                    TakeItemListFromProps(
                        subj=res,
                        obj=named_item_list,
                    )
                )
            elif isinstance(next_res, named(Behavior)):
                named_bvr = next_res
                result.append(
                    TakeBvrFromProps(
                        subj=res,
                        obj=named_bvr,
                    )
                )
            else:
                raise Exception(f"Unexpected resource sequence: {res}, {next_res}")
        else:
            raise Exception(f"Unexpected resource {res}")

    setattr(self, "_elements", result)
    return result


def _match_named_item(named_item, provided_named_item):
    return (
        provided_named_item.name == named_item.name
        and provided_named_item.typ.item_name == named_item.typ.item_name
    )


def pipeline_data_path(self, obj):
    result = ""
    elements = _get_elements(self)
    nr_elms = len(elements)

    for elm_idx in range(nr_elms):
        elm = elements[elm_idx]
        postfix = "?" if elm_idx < nr_elms - 1 else ""

        if isinstance(
            elm,
            (
                TakeItemListFromStateProvider,
                TakeItemFromStateProvider,
                TakeHighlightedElmFromStateProvider,
            ),
        ):
            result = f"props.{elm.obj.typ.ts_var}{postfix}" + result
        elif isinstance(elm, (TakeItemFromQuery, TakeItemListFromQuery)):
            query = elm.subj
            result = f"{query.name}.data?.{elm.obj.typ.ts_var}"
        elif isinstance(
            elm, (TakeItemFromProps, TakeItemListFromProps, TakeBvrFromProps)
        ):
            result = f"props.{elm.obj.typ.ts_var}{postfix}"
        elif isinstance(elm, (ExtractItemFromItem, ExtractItemListFromItem)):
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj.typ
            ).name
            result = f"{result}.{member}"
        else:
            raise Exception(f"Unexpected element {elm}")

        if elm.obj.typ is obj.typ:
            return result.removesuffix("?")

    return None


def pipeline_source(pipeline):
    if pipeline._root_query:
        return pipeline._root_query
    if pipeline._root_props:
        return pipeline._root_props
    elif pipeline._root_state_provider:
        return pipeline._root_state_provider
    raise Exception(
        f"No query or state in pipeline of component {pipeline.component}."
        + " Did you forget to add :props?"
    )


def pipeline_maybe_expression(pipeline, named_item_or_item_list):
    elements = _get_elements(pipeline)
    if pipeline._root_query:
        return pipeline._root_query.name
    elif pipeline._root_props:
        named_item = elements[0].obj
        if (
            named_item.name == named_item_or_item_list.name
            and named_item.typ == named_item_or_item_list.typ
        ):
            return None
        return f"props.{named_item.typ.item_name}"
    elif pipeline._root_state_provider:
        item_or_item_list = elements[0].obj
        if item_or_item_list.meta.term.tag in ("item", "item-list"):
            return f"state.{item_or_item_list.typ.ts_var}"
    else:
        raise Exception(f"Unknown pipeline source: {pipeline.source}")
