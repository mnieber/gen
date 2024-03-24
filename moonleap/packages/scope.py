from moonleap.packages.get_module_symbols import get_module_symbols
from moonleap.packages.rule import rule as rule_decorator
from moonleap.spec.rel import fuzzy_match
from moonleap.spec.term import match_term_to_pattern, patch_tag, str_to_term
from moonleap.utils.queue import Queue


class Scope:
    def __init__(self, name):
        self.name = name
        self.create_rule_by_term = {}
        self.rules = []
        self.base_tags_by_tag = {}

    def __repr__(self):
        return f"Scope: {self.name}"

    def add_rules(self, module):
        for f in get_module_symbols(module):
            if hasattr(f, "moonleap_create_rule_term"):
                term = f.moonleap_create_rule_term
                if term in self.create_rule_by_term:
                    raise Exception(
                        f"There can be only one creation rule for term: {term}"
                    )
                self.create_rule_by_term[term] = f

            if hasattr(f, "moonleap_rule"):
                self.rules.append(f.moonleap_rule)

        for res_term_str, rules in getattr(module, "rules", {}).items():
            for rel_tuple, f in rules.items():
                rule = rule_decorator(res_term_str, *rel_tuple)(f).moonleap_rule
                self.rules.append(rule)

        for tag, base_tags in getattr(module, "base_tags", {}).items():
            self.register_base_tags(tag, base_tags)

    def find_create_rule(self, subj_term):
        subj_base_tags = self.get_base_tags(subj_term)
        result = None
        result_term = None
        result_term_base_tags = []

        def _specificity_scores(term):
            # Lower scores are more specific.
            # E.g. (1, 2) means that term has one part more (or less) than subj_term,
            # and 2 x's are used to match term to subj_term.
            delta = len(term.parts) - len(subj_term.parts)
            return (abs(delta), term.parts.count("x"))

        for subj_base_tag in [None, *(subj_base_tags or [])]:
            patched_subj_term = patch_tag(subj_term, subj_base_tag)
            for term, rule in self.create_rule_by_term.items():
                if match_term_to_pattern(patched_subj_term, term):
                    if result_term and term.tag in result_term_base_tags:
                        continue

                    term_base_tags = self.get_base_tags(term, include_self=False)

                    if (
                        not result_term
                        or _specificity_scores(term) < _specificity_scores(result_term)
                        or (result_term.tag in term_base_tags)
                    ):
                        result = rule
                        result_term = term
                        result_term_base_tags = term_base_tags

        return result

    def find_rules(self, input_rel, subj_base_tags=None, obj_base_tags=None):
        return [
            rule
            for rule in self.rules
            if fuzzy_match(
                input_rel, rule.rel, subj_base_tags or [], obj_base_tags or []
            )
        ]

    def register_base_tags(self, tag, base_tags):
        self.base_tags_by_tag.setdefault(tag, []).extend(base_tags)

    def get_base_tags(self, term, include_self=True):
        result = []
        q = Queue(lambda x: x, [term.tag])
        for tag in q:
            result.append(tag)
            tags = self.base_tags_by_tag.get(tag, [])
            q.extend(tags)

        if not include_self:
            result.remove(term.tag)
        return result


def create(term_str):
    def wrapped(f):
        term = str_to_term(term_str, default_to_tag=True)
        f.moonleap_create_rule_term = term

        return f

    return wrapped
