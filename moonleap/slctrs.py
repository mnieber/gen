import ramda as R

from moonleap.parser.term import Term, fuzzy_match
from moonleap.rel import Rel


class RelSelector:
    def __init__(self, pattern_rel, fltr=None):
        self.pattern_rel = pattern_rel
        self.fltr = fltr or R.identity

    def select_from(self, resource):
        result = []

        for relation, object_resource in resource.get_relations():
            if fuzzy_match(relation, self.pattern_rel):
                result.append(object_resource)

        return self.fltr(result)


class PropSelector:
    def __init__(self, prop_name, fltr=None):
        self.prop_name = prop_name
        self.fltr = fltr or R.identity

    def select_from(self, resource):
        return self.fltr(getattr(resource, self.prop_name, []))


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
