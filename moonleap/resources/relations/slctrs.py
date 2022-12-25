import ramda as R

from moonleap.resources.relations.rel import fuzzy_match


class RelSelector:
    def __init__(self, pattern_rel, fltr=None):
        self.pattern_rel = pattern_rel
        self.fltr = fltr or R.identity

    def select_from(self, resource):
        result = []

        for relation, obj_res in resource.get_relations():
            if fuzzy_match(
                relation,
                self.pattern_rel,
                resource.meta.base_tags,
                obj_res.meta.base_tags,
            ):
                result.append(obj_res)

        return self.fltr(result)
