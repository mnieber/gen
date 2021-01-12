from dataclasses import dataclass

from moonleap.parser.term import Term, fuzzy_match


@dataclass(frozen=True)
class Rel:
    subj: Term = None
    verb: str = None
    obj: Term = None
    is_inv: bool = False

    def inv(self):
        return Rel(verb=self.verb, obj=self.obj, subj=self.subj, is_inv=not self.is_inv)


class RelSelector:
    def __init__(self, pattern_rel):
        self.pattern_rel = pattern_rel

    def select_from(self, resource):
        result = []

        for relation, object_resource in resource.get_relations():
            if fuzzy_match(relation, self.pattern_rel):
                result.append(object_resource)

        return result


class PropSelector:
    def __init__(self, prop_name):
        self.prop_name = prop_name

    def select_from(self, resource):
        return getattr(resource, self.prop_name, [])


class Selector:
    def __init__(self, slctrs):
        self.slctrs = slctrs

    def select_from(self, resource):
        result = [resource]

        for maybe_slctr in self.slctrs:
            next_result = []
            for rsrc in result:
                slctr = (
                    RelSelector(maybe_slctr)
                    if isinstance(maybe_slctr, Rel)
                    else maybe_slctr
                )
                next_result.extend(slctr.select_from(rsrc))
            result = next_result

        return result
