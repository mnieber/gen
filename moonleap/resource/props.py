import ramda as R
from moonleap.parser.term import maybe_term_to_term
from moonleap.resource import resolve
from moonleap.resource.prop import Prop
from moonleap.resource.rel import Rel, _is_intersecting
from moonleap.resource.slctrs import Selector
from moonleap.utils.inflect import singular


def fltr_instance(resource_type):
    resource_type = resolve(resource_type)
    return lambda x: isinstance(x, resource_type)


def child(verb, term, readonly=False, is_doc_prop=False, is_private_rel=False):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    slctr = Selector([rel])

    def get_child(self):
        children = slctr.select_from(self)
        if len(children) > 1:
            raise Exception(f"More than 1 child, verb={verb}, term={term}")

        return None if not children else children[0]

    def update_doc_meta(prop_name, doc_meta):
        if is_doc_prop:
            doc_meta.doc_prop(prop_name)
        if is_private_rel:
            doc_meta.private_rel(rel)

    return Prop(get_value=get_child, update_doc_meta=update_doc_meta)


def children(
    verb, term, read_only=False, rdcr=None, is_doc_prop=False, is_private_rel=False
):
    rel = Rel(verb=verb, obj=maybe_term_to_term(term))
    slctr = Selector([rel])

    def get_children(self):
        children = slctr.select_from(self)
        return rdcr(children) if rdcr else children

    def add_to_children(self, child):
        self.add_relation(rel, child)

    def update_doc_meta(prop_name, doc_meta):
        if is_doc_prop:
            doc_meta.doc_prop(prop_name)
        if is_private_rel:
            doc_meta.private_rel(rel)

    return Prop(
        get_value=get_children,
        add_value=None if read_only else add_to_children,
        update_doc_meta=update_doc_meta,
    )


def _fltr(resource_type):
    return R.filter(lambda x: isinstance(x, resource_type))


def parent(parent_resource_type, verb):
    parent_resource_type = resolve(parent_resource_type)

    def get_parent(self):
        parents = []
        for relation, object_resource in self.get_relations():
            if (
                relation.is_inv
                and isinstance(object_resource, parent_resource_type)
                and _is_intersecting(relation.verb, verb)
            ):
                if object_resource not in parents:
                    parents.append(object_resource)

        if len(parents) > 1:
            raise Exception("More than 1 parent")

        return None if not parents else parents[0]

    return Prop(get_value=get_parent)


def parents(
    parent_resource_type, verb, term, rdcr=None, is_doc_prop=False, is_private_rel=False
):
    parent_resource_type = resolve(parent_resource_type)
    rel = Rel(verb=verb, obj=maybe_term_to_term(term), is_inv=True)
    slctr = Selector([rel])

    def get_parents(self):
        parents = _fltr(parent_resource_type)(slctr.select_from(self))
        return rdcr(parents) if rdcr else parents

    def update_doc_meta(prop_name, doc_meta):
        if is_doc_prop:
            doc_meta.doc_prop(prop_name)
        if is_private_rel:
            doc_meta.private_rel(rel)

    return Prop(get_value=get_parents, update_doc_meta=update_doc_meta)


def tree(verb, term):
    children_prop = children(verb, term)
    sources_term = singular(term) + "-sources"
    sources_prop = children(verb, sources_term)

    def get_value(parent):
        class Inner:
            @property
            def merged(self):
                result = list(self.children)
                queue = list(self.sources)
                # never use the same source twice
                known_sources = list()

                while queue:
                    source = queue.pop(0)
                    if source not in known_sources:
                        known_sources.append(source)
                        queue.extend(sources_prop.get_value(source))
                        result.extend(children_prop.get_value(source))

                return result

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


def add_source(target_and_prop_name, source, description):
    target, prop_name = target_and_prop_name
    getattr(target, prop_name).add_source(source)
