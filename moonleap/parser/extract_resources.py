from importlib import import_module

from moonleap.always import Always, always_term
from moonleap.config import config


def create_resources(block):
    for line in block.lines:
        for term in line.terms:
            create_rule = config.create_rule_by_tag.get(term.tag)
            if not create_rule:
                continue

            if term in [x[0] for x in block.get_resource_by_term(include_parents=True)]:
                continue

            for resource in create_rule(term, line, block):
                if resource:
                    block.add_resource(resource, term)


def update_resources(block):
    parent_resource_by_term = [(always_term, Always())] + list(
        block.get_resource_by_term(include_parents=True)
    )
    resource_by_term = list(block.get_resource_by_term(include_parents=False))
    for parent_resource_term, parent_resource in parent_resource_by_term:
        update_rules = config.get_update_rules(parent_resource.type_id)
        for resource_type_id, update in update_rules.items():
            for resource_term, resource in resource_by_term:
                if resource_type_id == resource.type_id:
                    update(parent_resource, resource)
