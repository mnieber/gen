from moonleap.builder.install import get_symbols
from moonleap.builder.rule import rule as rule_decorator
from moonleap.resource.rel import fuzzy_match


class Scope:
    def __init__(self, name):
        self.name = name
        self.create_rule_by_term = {}
        self.rules = []
        self.base_tags_by_tag = {}

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
        result = None
        for term, rule in self.create_rule_by_term.items():
            if subj_term.tag == term.tag:
                if term.data:
                    if subj_term.data == term.data:
                        result = rule
                        break
                elif not result:
                    result = rule

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

    def get_base_tags(self, term):
        return self.base_tags_by_tag.get(term.tag, [])


def get_base_tags(resource):
    return resource.meta.base_tags if resource.meta else []
