import ramda as R

from moonleap.parser.term import Term, word_to_term
from moonleap.resource import resolve
from moonleap.slctrs import Rel, Selector


class Prop:
    def __init__(self, getter, setter=None, adder=None):
        self.get = getter
        self.set = setter
        self.add = adder


def fltr_instance(resource_type):
    resource_type = resolve(resource_type)
    return lambda x: isinstance(x, resource_type)


def maybe_term_to_term(maybe_term):
    if isinstance(maybe_term, Term):
        return maybe_term
    return word_to_term(maybe_term, default_to_tag=True)


def child(verb, term):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    slctr = Selector([rel])

    def get_child(self):
        children = slctr.select_from(self)
        if len(children) > 1:
            raise Exception(f"More than 1 child, verb={verb}, term={term}")

        return None if not children else children[0]

    def set_child(self, child):
        children = slctr.select_from(self)
        if len(children) > 0:
            raise Exception("Already has a child")

        child.block = self.block
        child.term = self.term
        self.add_relation(rel, child)

    return Prop(get_child, setter=set_child)


def children(verb, term, rdcr=None):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    slctr = Selector([rel])

    def get_children(self):
        children = slctr.select_from(self)
        return rdcr(children) if rdcr else children

    def add_to_children(self, child):
        self.add_relation(rel, child)

    return Prop(get_children, adder=add_to_children)


def _fltr(resource_type):
    return R.filter(lambda x: isinstance(x, resource_type))


def parent(parent_resource_type, verb, term):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    slctr = Selector([rel.inv()])

    def get_parent(self):
        parents = _fltr(parent_resource_type)(slctr.select_from(self))
        if len(parents) > 1:
            raise Exception("More than 1 parent")

        return None if not parents else parents[0]

    return Prop(get_parent)


def parents(parent_resource_type, rel, rdcr=None):
    slctr = Selector([rel.inv()])

    def get_parents(self):
        parents = _fltr(parent_resource_type)(slctr.select_from(self))
        return rdcr(parents) if rdcr else parents

    return Prop(get_parents)
