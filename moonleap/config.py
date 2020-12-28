from ramda import merge

from moonleap.utils import str_to_type_id


class Config:
    def __init__(self):
        self.create_rule_by_tag = {}
        self.update_rules_by_resource_type_id = {}
        self.is_ittable_by_tag = {}

    def get_update_rules(self, resource):
        return self.update_rules_by_resource_type_id.get(resource.type_id) or []


config = Config()


def install(module):
    config.create_rule_by_tag = merge(
        config.create_rule_by_tag, module.create_rule_by_tag
    )

    resource_type_id = str_to_type_id(module.__package__)
    if hasattr(module, "update_rules"):
        config.update_rules_by_resource_type_id = merge(
            config.update_rules_by_resource_type_id,
            {resource_type_id: module.update_rules},
        )

    if hasattr(module, "is_ittable_by_tag"):
        config.is_ittable_by_tag = merge(
            config.is_ittable_by_tag,
            module.is_ittable_by_tag,
        )
