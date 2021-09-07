from moonleap.builder.install import get_symbols
from moonleap.builder.rule import rule as rule_decorator
from moonleap.resource.rel import fuzzy_match


class Scope:
    def __init__(self, name):
        self.name = name
        self.create_rule_by_term = {}
        self.rules = []

    def add_rules(self, module):
        for f in get_symbols(module):
            if hasattr(f, "moonleap_create_rule_term"):
                term, base_tags = f.moonleap_create_rule_term
                if term in self.create_rule_by_term:
                    raise Exception(
                        f"There can be only one creation rule for term: {term}"
                    )
                self.create_rule_by_term[term] = f, base_tags

            if hasattr(f, "moonleap_rule"):
                self.rules.append(f.moonleap_rule)

        for rel_tuple, f in getattr(module, "rules", []):
            rule = rule_decorator(*rel_tuple)(f).moonleap_rule
            self.rules.append(rule)

    def find_create_rule(self, subj_term):
        result = None
        for term, rule in self.create_rule_by_term.items():
            if subj_term.tag == term.tag:
                if term.data:
                    if subj_term.data == term.data:
                        result = rule
                        break
                elif not result:
                    result = rule

        return result or (None, None)

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
