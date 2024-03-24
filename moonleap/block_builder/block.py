import typing as T

from moonleap.spec.line import Line
from moonleap.spec.term import Term


def _get_base_tags(term, block, include_self):
    from moonleap.utils.fp import uniq

    result = []

    for scope in block.get_scopes():
        result.extend(scope.get_base_tags(term, include_self))

    return uniq(result)


class Block:
    def __init__(self, name, level, scope_names):
        self.name = name
        self.scope_names = scope_names
        self._scopes = []
        self.level = level
        self.parent_block = None
        self.child_blocks = []
        self._resource_by_term = []
        self._relation_tokens = []
        self.lines: T.List[Line] = []
        self._dbg_text = ""

    @property
    def title_line(self):
        return self.lines[0] if self.lines else None

    def get_scopes(self):
        return self._scopes

    def set_scopes(self, scopes):
        self._scopes = scopes

    def has_relation(self, relation):
        return _get_token(relation) in self._relation_tokens

    def register_relation(self, relation):
        if not self.has_relation(relation):
            self._relation_tokens.append(_get_token(relation))

    def describes(self, term):
        def stem_term(term):
            pos = term.tag.find("~")
            tag = term.tag[:pos] if pos != -1 else term.tag
            return Term(parts=(*term.parts[:-1], tag))

        if term.name is not None:
            return False

        stemmed_term = stem_term(term)
        for line in self.lines:
            for t in line.terms:
                is_title = line is self.title_line or t.is_title
                if is_title and stem_term(t) == stemmed_term:
                    return True

        for base_tag in _get_base_tags(stemmed_term, self, False):
            if self.describes(Term(parts=(base_tag,))):
                return True

        return False

    def get_resource(self, term):
        result = None
        for t, res, _ in self._resource_by_term:
            if t == term:
                if result:
                    raise Exception(
                        f"Multiple resources for term {term} in block {self.name}"
                    )
                result = res

        return result

    def link(self, parent_block):
        self.parent_block = parent_block
        if parent_block:
            parent_block.child_blocks.append(self)

    def get_blocks(
        self, include_self=True, include_children=False, include_parents=False
    ):
        result = []

        if include_parents and self.parent_block:
            result += self.parent_block.get_blocks(include_parents=True)

        if include_self:
            result += [self]

        if include_children:
            for child_block in self.child_blocks:
                result += child_block.get_blocks(include_children=True)

        return result

    def get_resource_by_term(self):
        return [x for x in self._resource_by_term]

    def add_resource_for_term(self, resource, term, is_owner):
        existing_resource = self.get_resource(term)
        if existing_resource is resource:
            return
        elif existing_resource:
            raise Exception(f"Block {self.name} already has a resource for term {term}")

        self._resource_by_term.append((term, resource, is_owner))

    def drop_resource(self, resource):
        self._resource_by_term = [
            x for x in self._resource_by_term if x[1] is not resource
        ]

    def __repr__(self):
        return f"Block ({self.name})"


def _get_token(relation):
    return (relation.subj, relation.verb, relation.obj)
