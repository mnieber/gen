import typing as T
from dataclasses import dataclass

from moonleap import Resource, named
from moonleap.parser.term import match_term_to_pattern
from moonleap.utils.fp import aperture
from titan.api_pkg.mutation.resources import Mutation
from titan.api_pkg.pipeline.resources import PropsSource
from titan.api_pkg.query.resources import Query
from titan.types_pkg.item.resources import Item
from titan.types_pkg.itemlist.resources import ItemList
from titan.types_pkg.pkg.get_member_field_spec import get_member_field_spec


@dataclass
class PipelineElement:
    obj: T.Optional[Resource] = None
    subj: T.Optional[Resource] = None


class TakeItemListFromStateProvider(PipelineElement):
    pass


class TakeItemFromStateProvider(PipelineElement):
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


def elements(self):
    from titan.react_view_pkg.stateprovider.resources import StateProvider

    if hasattr(self, "_elements"):
        return self._elements

    resources = list(self.resources)

    if self.root_query:
        resources.insert(0, self.root_query)
    elif self.root_state_provider:
        resources.insert(0, self.root_state_provider)
    elif self.root_props:
        resources.insert(0, self.root_props)
    else:
        raise Exception("No query or state")

    _source_pipeline = None

    result = []
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
            else:
                raise Exception(f"Unexpected resource sequence: {res}, {next_res}")
        else:
            raise Exception(f"Unexpected resource {res}")

    setattr(self, "_elements", result)
    setattr(self, "_source_pipeline", _source_pipeline)
    return result


def _match_named_item(named_item, provided_named_item):
    return (
        provided_named_item.name == named_item.name
        and provided_named_item.typ.item_name == named_item.typ.item_name
    )


def output(self):
    named_res = self.resources[-1]
    assert isinstance(named_res, (named(Item), named(ItemList)))
    return named_res


def output_name(self):
    return self.output.name or self.output.typ.ts_var


def deleter_mutation(self):
    for bvr in self.bvrs:
        if bvr.name == "delete":
            return bvr
    return None


def data_path(self, obj=None, obj_term=None):
    result = ""
    nr_elms = len(self.elements)

    for elm_idx in range(nr_elms):
        elm = self.elements[elm_idx]
        if isinstance(
            elm,
            (
                TakeItemListFromStateProvider,
                TakeItemFromStateProvider,
                TakeHighlightedElmFromStateProvider,
            ),
        ):
            postfix = "?" if elm_idx < nr_elms - 1 else ""
            result = f"props.{elm.obj.typ.ts_var}{postfix}" + result
        elif isinstance(elm, (TakeItemFromQuery, TakeItemListFromQuery)):
            query = elm.subj
            result = f"{query.name}.data?.{elm.obj.typ.ts_var}"
        elif isinstance(elm, (TakeItemFromProps, TakeItemListFromProps)):
            result = f"props.{elm.obj.typ.ts_var}"
        elif isinstance(elm, (ExtractItemFromItem, ExtractItemListFromItem)):
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj.typ
            ).name
            result = f"{result}.{member}"
        else:
            raise Exception(f"Unexpected element {elm}")

        if (obj and elm.obj.typ is obj.typ) or (
            obj_term and match_term_to_pattern(elm.obj.meta.term, obj_term)
        ):
            return result.removesuffix("?")

    return None if (obj or obj_term) else result


def status_expression(self):
    elm = self.elements[0]
    if isinstance(
        elm,
        (
            TakeItemListFromStateProvider,
            TakeItemFromStateProvider,
            TakeHighlightedElmFromStateProvider,
        ),
    ):
        return f"props.{elm.obj.typ.ts_var}RS"
    elif isinstance(elm, (TakeItemFromQuery, TakeItemListFromQuery)):
        query = elm.subj
        return f"{query.name}.status"

    assert False


def root_pipeline(self):
    if not self.root_state_provider:
        return self

    for p in self.root_state_provider.pipelines:
        if p.output == self.resources[-1].typ:
            return p

    raise Exception("No root pipeline")


def pipeline_source(pipeline):
    if pipeline.root_query:
        return pipeline.root_query
    if pipeline.root_props:
        return pipeline.root_props
    elif pipeline.root_state_provider:
        return pipeline.root_state_provider
    raise Exception("Unknown pipeline source")
