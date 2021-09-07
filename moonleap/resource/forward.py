import typing as T

from moonleap.parser.term import Term, word_to_term
from moonleap.resource import Resource
from moonleap.resource.rel import Rel


def _to_term(x: T.Union[Term, str]) -> Term:
    if isinstance(x, Term):
        return x

    term = word_to_term(x)
    if term is None:
        raise Exception("Cannot perform _to_term on {x}")
    return term


def create_forward(
    subj: T.Union[Term, str, Resource],
    verb: T.Union[str, T.Tuple[str, ...]],
    obj: T.Union[Term, str],
):
    if subj is None:
        raise Exception("Subject is None")

    if obj is None:
        raise Exception("Object is None")

    if isinstance(subj, str):
        subj = word_to_term(subj, default_to_tag=True)

    if isinstance(subj, Resource):
        subj = subj._meta.term

    return Rel(subj=subj, verb=verb, obj=_to_term(obj))


def to_list_of_relations(x, rule):
    result = list(x) if (isinstance(x, list) or isinstance(x, tuple)) else [x]
    for rel in result:
        if not isinstance(rel, Rel):
            raise Exception(
                f"A rule ({rule}) should either return a Rel or a list of Rel"
            )
    return result
