import ramda as R

from moonleap.parser.term import Term, word_to_term
from moonleap.prop import Prop
from moonleap.rel import Rel
from moonleap.resource import resolve
from moonleap.slctrs import Selector
from moonleap.utils.inflect import singular


def fltr_instance(resource_type):
    resource_type = resolve(resource_type)
    return lambda x: isinstance(x, resource_type)


def maybe_term_to_term(maybe_term):
    if isinstance(maybe_term, Term):
        return maybe_term
    return word_to_term(maybe_term, default_to_tag=True)


def child(verb, term, is_doc=True):
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

    return Prop(
        get_value=get_child, set_value=set_child, doc_as_rel=rel if is_doc else None
    )


def children(verb, term, rdcr=None, is_doc=True):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    slctr = Selector([rel])

    def get_children(self):
        children = slctr.select_from(self)
        return rdcr(children) if rdcr else children

    def add_to_children(self, child):
        self.add_relation(rel, child)

    return Prop(
        get_value=get_children,
        add_value=add_to_children,
        doc_as_rel=rel if is_doc else None,
    )


def _fltr(resource_type):
    return R.filter(lambda x: isinstance(x, resource_type))


def parent(parent_resource_type, verb, term, is_doc=True):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term), is_inv=True)
    slctr = Selector([rel])

    def get_parent(self):
        parents = _fltr(parent_resource_type)(slctr.select_from(self))
        if len(parents) > 1:
            raise Exception("More than 1 parent")

        return None if not parents else parents[0]

    return Prop(get_value=get_parent, doc_as_rel=rel if is_doc else None)


def parents(parent_resource_type, verb, term, rdcr=None, is_doc=True):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term), is_inv=True)
    slctr = Selector([rel])

    def get_parents(self):
        parents = _fltr(parent_resource_type)(slctr.select_from(self))
        return rdcr(parents) if rdcr else parents

    return Prop(get_value=get_parents, doc_as_rel=rel if is_doc else None)


def tree(verb, term, merge, initial):
    rdcr = R.reduce(merge, initial)
    children_prop = children(verb, term)
    sources_term = singular(term) + "-sources"
    sources_prop = children(verb, sources_term)

    def get_value(parent):
        class Inner:
            @property
            def merged(self):
                result = list(self.children)
                queue = list(self.sources)

                while queue:
                    source = queue.pop(0)
                    queue.extend(sources_prop.get_value(source))
                    result.extend(children_prop.get_value(source))

                return rdcr(result)

            @property
            def children(self):
                return children_prop.get_value(parent)

            @property
            def sources(self):
                return sources_prop.get_value(parent)

            def add(self, child):
                children_prop.add_value(parent, child)

            def add_source(self, source):
                sources_prop.add_value(parent, source)

        return Inner()

    return Prop(get_value)
