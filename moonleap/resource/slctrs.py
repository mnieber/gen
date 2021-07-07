import ramda as R
from moonleap.resource.rel import Rel, fuzzy_match


class RelSelector:
    def __init__(self, pattern_rel, fltr=None):
        self.pattern_rel = pattern_rel
        self.fltr = fltr or R.identity

    def select_from(self, resource):
        result = []

        for relation, obj_resource in resource.get_relations():
            if fuzzy_match(relation, self.pattern_rel):
                result.append(obj_resource)

        return self.fltr(result)


class PropSelector:
    def __init__(self, getter, fltr=None):
        self.getter = getter
        self.fltr = fltr or R.identity

    def select_from(self, resource):
        return self.fltr(self.getter(resource))


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
