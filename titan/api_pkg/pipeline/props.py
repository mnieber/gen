import typing as T
from dataclasses import dataclass

from moonleap import Resource, Term, named
from moonleap.typespec.get_member_field_spec import get_member_field_spec
from moonleap.utils.fp import aperture
from moonleap.utils.join import join
from titan.api_pkg.item.resources import Item
from titan.api_pkg.itemlist.resources import ItemList
from titan.api_pkg.mutation.resources import Mutation
from titan.api_pkg.query.resources import Query


def get_select_item_effect_term(item):
    name_postfix = join("-by-", "-and-".join(item.type_spec.select_item_by))
    return Term(f"select-{item.meta.term.data}{name_postfix}", "select-item-effect")


@dataclass
class PipelineElement:
    obj: T.Optional[Resource] = None
    subj: T.Optional[Resource] = None


class TakeItemListFromState(PipelineElement):
    pass


class TakeItemFromState(PipelineElement):
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
class TakeHighlightedElmFromState(PipelineElement):
    item_list: T.Any = None


class StoreItemInState(PipelineElement):
    pass


class StoreItemListInState(PipelineElement):
    pass


def elements(self):
    from titan.react_view_pkg.state.resources import State

    if hasattr(self, "_elements"):
        return self._elements

    resources = list(self.resources)

    result = []
    if self.root_query:
        resources.insert(0, self.root_query)
    elif self.root_state:
        resources.insert(0, self.root_state)
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

        elif isinstance(res, State):
            state = res
            if isinstance(next_res, named(Item)):
                named_item = next_res
                pipelines = [p for p in state.pipelines if p.output == named_item.typ]
                if pipelines:
                    if _source_pipeline:
                        raise Exception("Multiple source pipelines")
                    _source_pipeline = pipelines[0]
                    result.append(
                        TakeItemFromState(
                            subj=state,
                            obj=named_item.typ,
                        )
                    )
                else:
                    pipelines = [
                        p
                        for p in state.pipelines
                        if isinstance(p.output, ItemList) and p.output.item == item
                    ]
                    found = False
                    for p in pipelines:
                        if p.get_bvr("highlight"):
                            found = True
                            result.append(
                                TakeHighlightedElmFromState(
                                    subj=state, item_list=p.output, obj=item
                                )
                            )
                    if not found:
                        raise Exception(f"Cannot take {next_res} from state {res}")

            elif isinstance(next_res, named(ItemList)):
                item_list = next_res.typ
                result.append(
                    TakeItemListFromState(
                        subj=state,
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


def output(self):
    named_res = self.resources[-1]
    assert isinstance(named_res, (named(Item), named(ItemList)))
    return self.resources[-1].typ


def deleter_mutation(self):
    for bvr in self.bvrs:
        if bvr.name == "delete":
            return bvr
    return None


def bvrs(self):
    named_res = self.resources[-1]
    assert isinstance(named_res, (named(Item), named(ItemList)))
    return named_res.bvrs if isinstance(named_res, named(ItemList)) else []


def get_bvr(self, name):
    for bvr in self.bvrs:
        if bvr.name == name:
            return bvr
    return None


def input_expression(self):
    result = ""
    nr_elms = len(self.elements)

    for elm_idx in range(nr_elms):
        elm = self.elements[elm_idx]
        if isinstance(
            elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
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
        elm, (TakeItemListFromState, TakeItemFromState, TakeHighlightedElmFromState)
    ):
        return f"props.{elm.obj.ts_var}RS"
    elif isinstance(elm, (TakeItemFromQuery, TakeItemListFromQuery)):
        query = elm.subj
        return f"{query.name}.status"

    assert False


def root_pipeline(self):
    if not self.root_state:
        return self

    for p in self.root_state.pipelines:
        if p.output == self.resources[-1].typ:
            return p

    raise Exception("No root pipeline")
