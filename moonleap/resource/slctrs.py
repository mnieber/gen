import ramda as R
from moonleap.resource.rel import fuzzy_match


class RelSelector:
    def __init__(self, pattern_rel, fltr=None):
        self.pattern_rel = pattern_rel
        self.fltr = fltr or R.identity

    def select_from(self, resource):
        result = []

        for relation, obj_resource in resource.get_relations():
            if fuzzy_match(
                relation,
                self.pattern_rel,
                resource._meta.base_tags,
                obj_resource._meta.base_tags,
            ):
                result.append(obj_resource)

        return self.fltr(result)
