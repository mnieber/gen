from importlib import import_module

from moonleap.config import config


def create_resources(block):
    for line in block.lines:
        for term in line.terms:
            create_rule = config.create_rule_by_tag.get(term.tag)
            if not create_rule:
                continue

            if term in block.get_terms(include_parents=True):
                continue

            for resource in create_rule(term, line, block):
                block.add_resource(resource, term)


def update_resources(block):
    resource_by_term = list(block.get_resource_by_term(include_parents=False))
    for resource_term, resource in resource_by_term:
        update_rules = config.get_update_rules(resource)
        for resource_type_id, update in update_rules.items():
            for co_resource_term, co_resource in block.get_resource_by_term(
                include_parents=True
            ):
                if resource_type_id == co_resource.type_id:
                    update(resource, co_resource)
