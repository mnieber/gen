import typing as T
from dataclasses import dataclass

from moonleap import Resource, named
from moonleap.utils.fp import aperture
from titan.api_pkg.mutation.resources import Mutation
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

    result = []
    if self.root_query:
        resources.insert(0, self.root_query)
    elif self.root_state_provider:
        resources.insert(0, self.root_state_provider)
    else:
        raise Exception("No query or state")

    _source_pipeline = None

    for res, next_res in aperture(2, resources):
        if isinstance(res, (Query, Mutation)):
            query = res
            if isinstance(next_res, named(Item)):
                named_item = next_res
                result.append(
                    TakeItemFromQuery(
                        subj=query,
                        obj=named_item.typ,
                    )
                )
            elif isinstance(next_res, named(ItemList)):
                named_item_list = next_res
                result.append(
                    TakeItemListFromQuery(
                        subj=query,
                        obj=named_item_list.typ,
                    )
                )
            else:
                raise Exception(f"Unexpected resource sequence: {res}, {next_res}")

        elif isinstance(res, StateProvider):
            state_provider = res
            if isinstance(next_res, named(Item)):
                found = False
                named_item = next_res
                for provided_named_item in state_provider.named_items:
                    if _match_named_item(named_item, provided_named_item):
                        found = True
                        result.append(
                            TakeItemFromStateProvider(
                                subj=state_provider,
                                obj=named_item.typ,
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
                                    obj=named_item.typ,
                                )
                            )

                if not found:
                    raise Exception(
                        f"Cannot take {next_res} from state provider {state_provider}"
                    )

            elif isinstance(next_res, named(ItemList)):
                item_list = next_res.typ
                result.append(
                    TakeItemListFromState(
                        subj=state_provider.state,
                        obj=item_list,
                    )
                )
            else:
                raise Exception(f"Unexpected resource sequence: {res}, {next_res}")

        elif isinstance(res, named(Item)):
            item = res.typ
            if isinstance(next_res, named(Item)):
                result.append(
                    ExtractItemFromItem(
                        subj=item,
                        obj=next_res.typ,
                    )
                )
            elif isinstance(next_res, named(ItemList)):
                result.append(
                    ExtractItemListFromItem(
                        subj=item,
                        obj=next_res.typ,
                    )
                )
            else:
                raise Exception(f"Unexpected resource sequence: {res}, {next_res}")
        elif isinstance(res, named(ItemList)):
            raise NotImplementedError(f"{res}")
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


def bvrs(self):
    return []


def get_bvr(self, name):
    for bvr in self.bvrs:
        if bvr.name == name:
            return bvr
    return None


def result_expression(self):
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
            result = f"props.{elm.obj.ts_var}{postfix}" + result
        elif isinstance(elm, (TakeItemFromQuery, TakeItemListFromQuery)):
            query = elm.subj
            result = f"{query.name}.data?.{elm.obj.ts_var}"
        elif isinstance(elm, (ExtractItemFromItem, ExtractItemListFromItem)):
            member = get_member_field_spec(
                parent_item=elm.subj, member_item=elm.obj
            ).name
            result = f"{result}.{member}"
    return result


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
        return f"props.{elm.obj.ts_var}RS"
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
    elif pipeline.root_state_provider:
        pipeline_elm = pipeline.elements[1]
        if isinstance(
            pipeline_elm,
            (
                TakeItemFromStateProvider,
                TakeHighlightedElmFromStateProvider,
                ExtractItemListFromItem,
                TakeItemListFromStateProvider,
            ),
        ):
            return pipeline_elm.subj
    raise Exception("Unknown pipeline source")
