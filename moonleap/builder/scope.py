from moonleap.builder.install import get_symbols
from moonleap.builder.rule import rule as rule_decorator
from moonleap.parser.term import match_term_to_pattern, patch_tag
from moonleap.resource.rel import fuzzy_match
from moonleap.utils.queue import Queue


class Scope:
    def __init__(self, name):
        self.name = name
        self.create_rule_by_term = {}
        self.rules = []
        self.base_tags_by_tag = {}

    def __str__(self):
        return f"Scope: {self.name}"

    def add_rules(self, module):
        for f in get_symbols(module):
            if hasattr(f, "moonleap_create_rule_term"):
                term = f.moonleap_create_rule_term
                if term in self.create_rule_by_term:
                    raise Exception(
                        f"There can be only one creation rule for term: {term}"
                    )
                self.create_rule_by_term[term] = f

            if hasattr(f, "moonleap_rule"):
                self.rules.append(f.moonleap_rule)

        for rel_tuple, f in getattr(module, "rules", []):
            rule = rule_decorator(*rel_tuple)(f).moonleap_rule
            self.rules.append(rule)

        for tag, base_tags in getattr(module, "base_tags", []):
            self.register_base_tags(tag, base_tags)

    def find_create_rule(self, subj_term):
        subj_base_tags = self.get_base_tags(subj_term)
        result = None
        result_term = None
        result_term_base_tags = []

        for subj_base_tag in [None, *(subj_base_tags or [])]:
            patched_subj_term = patch_tag(subj_term, subj_base_tag)
            for term, rule in self.create_rule_by_term.items():
                if match_term_to_pattern(patched_subj_term, term):
                    if result_term and term.tag in result_term_base_tags:
                        continue

                    term_base_tags = self.get_base_tags(term, include_self=False)

                    if (
                        not result_term
                        or (result_term.data == "x" and term.data != "x")
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

    def drop_rule(self, rule):
        self.rules = [x for x in self.rules if x is not rule]

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


def get_base_tags(resource):
    return resource.meta.base_tags if resource.meta else []
