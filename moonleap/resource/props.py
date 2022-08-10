import typing as T
from dataclasses import dataclass

from moonleap.parser.term import Term, word_to_term
from moonleap.resource.prop import Prop
from moonleap.resource.rel import Rel, fuzzy_match
from moonleap.resource.slctrs import RelSelector


@dataclass
class RelationNotFound(Exception):
    subj: T.Any
    verb: str
    obj: T.Any

    def __str__(self):
        return f"Not found: {self.subj} /{self.verb} {self.obj}"


class ChildNotFound(RelationNotFound):
    pass


class ParentNotFound(RelationNotFound):
    pass


def child(verb, term, required=False):
    rel = Rel(
        verb=verb,
        obj=term if isinstance(term, Term) else word_to_term(term, default_to_tag=True),
    )
    slctr = RelSelector(rel)

    def get_child(self):
        children = slctr.select_from(self)

        if len(children) > 1:
            raise Exception(f"More than 1 child, verb={verb}, term={term}")

        if required and not children:
            raise ChildNotFound(subj=self, verb=verb, obj=rel.obj)

        return None if not children else children[0]

    return Prop(get_value=get_child)


def children(verb, term, rdcr=None):
    rel = Rel(
        verb=verb,
        obj=term if isinstance(term, Term) else word_to_term(term, default_to_tag=True),
    )
    slctr = RelSelector(rel)

    def get_children(self):
        children = slctr.select_from(self)
        return rdcr(children) if rdcr else children

    return Prop(get_value=get_children)


def _get_parents(parent_term_str, verb, child_term, inv_relations):
    parents = []
    pattern_rel = Rel(word_to_term(parent_term_str, True), verb, child_term)
    for rel, subj_res in inv_relations:
        if fuzzy_match(rel, pattern_rel, subj_res.meta.base_tags, []):
            if subj_res not in parents:
                parents.append(subj_res)
    return parents


def parent(parent_term_str, verb, required=False):
    def get_parent(self):
        parents = _get_parents(
            parent_term_str, verb, self.meta.term, self.get_inv_relations()
        )

        if len(parents) > 1:
            raise Exception("More than 1 parent")
        elif required and not parents:
            raise ParentNotFound(subj=parent_term_str, verb=verb, obj=self)

        return None if not parents else parents[0]

    return Prop(get_value=get_parent)


def parents(parent_term_str, verb):
    def get_parent(self):
        return _get_parents(
            parent_term_str, verb, self.meta.term, self.get_inv_relations()
        )

    return Prop(get_value=get_parent)


def empty_rule():
    return lambda *args, **kwargs: None
