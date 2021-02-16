from moonleap.resource.rel import fuzzy_match


class Config:
    def __init__(self):
        self.create_rule_by_term = {}
        self.rules = []

    def get_create_rule(self, subj_term):
        result = None
        for term, rule in config.create_rule_by_term.items():
            if subj_term.tag == term.tag:
                if term.data:
                    if subj_term.data == term.data:
                        return rule
                elif not result:
                    result = rule
        return result

    def get_rules(self, input_rel):
        return [rule for rule in self.rules if fuzzy_match(input_rel, rule.rel)]

    def add_rule(self, rule):
        self.rules.append(rule)


config = Config()
