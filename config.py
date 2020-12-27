from ramda import merge


class Config:
    def __init__(self):
        self.create_rule_by_tag = {}
        self.update_rules = {}
        self.ittable_lut = {}


config = Config()


def install(module):
    config.create_rule_by_tag = merge(
        config.create_rule_by_tag, module.create_rule_by_tag
    )
    config.update_rules = merge(config.update_rules, module.update_rules)
