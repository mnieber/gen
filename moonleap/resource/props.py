import typing as T
from dataclasses import dataclass

from moonleap.builder.scope import get_base_tags
from moonleap.parser.term import maybe_term_to_term, word_to_term
from moonleap.resource.prop import Prop
from moonleap.resource.rel import Rel, fuzzy_match
from moonleap.resource.slctrs import RelSelector
from moonleap.utils.inflect import singular
from moonleap.utils.queue import Queue


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
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
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
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    slctr = RelSelector(rel)

    def get_children(self):
        children = slctr.select_from(self)
        return rdcr(children) if rdcr else children

    return Prop(get_value=get_children)


def _get_parents(parent_term_str, verb, child_term, inv_relations):
    parents = []
    pattern_rel = Rel(word_to_term(parent_term_str, True), verb, child_term)
    for rel, subj_res in inv_relations:
        if fuzzy_match(rel, pattern_rel, get_base_tags(subj_res), []):
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


def tree(verb, term):
    children_prop = children(verb, term)
    children_prop_rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    sources_term = singular(term) + "-sources"
    sources_prop = children(verb, sources_term)
    sources_prop_rel = Rel(verb=verb, obj=maybe_term_to_term(sources_term))

    def get_value(parent):
        class Inner:
            @property
            def merged(self):
                result = []
                queue = Queue(lambda x: x, [parent])
                for source in queue:
                    result.extend(children_prop.get_value(source))
                    queue.extend(sources_prop.get_value(source))
                return result

            @property
            def children(self):
                return children_prop.get_value(parent)

            @property
            def sources(self):
                return sources_prop.get_value(parent)

            def add(self, child):
                parent.add_relation(children_prop_rel, child)

            def add_source(self, source):
                parent.add_relation(sources_prop_rel, source)

        return Inner()

    return Prop(get_value)


def receives(prop_name):
    def f(subj, obj):
        getattr(subj, prop_name).add_source(obj)

    return f


def feeds(prop_name):
    def f(subj, obj):
        getattr(obj, prop_name).add_source(subj)

    return f


def empty_rule():
    return lambda *args, **kwargs: None
