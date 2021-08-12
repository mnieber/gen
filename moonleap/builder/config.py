import bisect

from moonleap.builder.install import get_empty_rules, get_symbols
from moonleap.parser.term import word_to_term
from moonleap.resource.rel import fuzzy_match


class Scope:
    def __init__(self, name):
        self.name = name
        self.create_rule_by_term = {}
        self.rules = []

    def add_rules(self, module):
        for f in get_symbols(module):
            if hasattr(f, "moonleap_create_rule_by_tag"):
                for tag, create_rule in f.moonleap_create_rule_by_tag.items():
                    term = word_to_term(tag, default_to_tag=True)
                    self.create_rule_by_term[term] = create_rule

            if hasattr(f, "moonleap_rule"):
                bisect.insort(self.rules, f.moonleap_rule)

        for rule in get_empty_rules(module):
            bisect.insort(self.rules, rule)

    def get_create_rule(self, subj_term):
        result = None
        for term, rule in self.create_rule_by_term.items():
            if subj_term.tag == term.tag:
                if term.data:
                    if subj_term.data == term.data:
                        return rule
                elif not result:
                    result = rule
        return result

    def get_rules(self, input_rel):
        return [rule for rule in self.rules if fuzzy_match(input_rel, rule.rel)]

    def drop_rule(self, rule):
        self.rules = [x for x in self.rules if x is not rule]
