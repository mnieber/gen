import typing as T

from moonleap.resources.resource import Resource
from moonleap.spec.rel import Rel
from moonleap.spec.term import Term, str_to_term


def _to_term(x: T.Union[Term, str]) -> Term:
    if isinstance(x, Term):
        return x

    term = str_to_term(x)
    if term is None:
        raise Exception(f"Cannot perform _to_term on {x}")
    return term


def create_forward(
    subj: T.Union[Term, str, Resource],
    verb: T.Union[str, T.Tuple[str, ...]],
    obj: T.Union[Term, str, Resource],
    origin: T.Any = None,
):
    if subj is None:
        raise Exception("Subject is None")

    if obj is None:
        raise Exception("Object is None")

    if isinstance(subj, str):
        subj = _to_term(subj)

    if isinstance(obj, str):
        obj = _to_term(obj)

    subj_res = None
    if isinstance(subj, Resource):
        subj_res = subj
        subj = subj_res.meta.term

    obj_res = None
    if isinstance(obj, Resource):
        obj_res = obj
        obj = obj_res.meta.term

    return Rel(
        subj=subj,
        subj_res=subj_res,
        verb=verb,
        obj=obj,
        obj_res=obj_res,
        origin=origin,
    )
