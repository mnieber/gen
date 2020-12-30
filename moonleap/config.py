from ramda import merge

from moonleap.utils import str_to_type_id


class Config:
    def __init__(self):
        self.create_rule_by_tag = {}
        self.update_rules_by_resource_type_id = {}
        self.is_ittable_by_tag = {}

    def get_update_rules(self, resource):
        return self.update_rules_by_resource_type_id.get(resource.type_id) or {}


config = Config()


def install(module):
    for tag in module.tags:
        config.create_rule_by_tag[tag] = module.create
        config.is_ittable_by_tag[tag] = getattr(module, "is_ittable", False)


def reduce(resource, resource_id):
    this_resource_id = str_to_type_id(resource.__module__)

    def wrapped(f):
        config.update_rules_by_resource_type_id.setdefault(this_resource_id, {})
        config.update_rules_by_resource_type_id[this_resource_id][resource_id] = f

    return wrapped
