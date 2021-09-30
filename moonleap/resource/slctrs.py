import ramda as R
from moonleap.resource.rel import fuzzy_match


class RelSelector:
    def __init__(self, pattern_rel, fltr=None):
        self.pattern_rel = pattern_rel
        self.fltr = fltr or R.identity

    def select_from(self, resource):
        from moonleap.builder.scope import get_base_tags

        result = []

        for relation, obj_res in resource.get_relations():
            if fuzzy_match(
                relation,
                self.pattern_rel,
                get_base_tags(resource),
                get_base_tags(obj_res),
            ):
                result.append(obj_res)

        return self.fltr(result)
