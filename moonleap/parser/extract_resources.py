from importlib import import_module

from moonleap.config import config
from moonleap.parser.term import always_term
from moonleap.resource import Always


def skip_term(block, term):
    return term in [x[0] for x in block.get_resource_by_term(include_parents=True)]


def update_parent_resources(block, resource):
    new_resources = []

    parent_resource_by_term = [(always_term, Always())] + list(
        block.get_resource_by_term(include_parents=True)
    )
    for parent_resource_term, parent_resource in parent_resource_by_term:
        update_rules = config.get_update_rules(parent_resource.type_id)
        for resource_type_id, update in update_rules.items():
            if resource_type_id == resource.type_id:
                new_resources += update(parent_resource, resource) or []

    for new_resource in new_resources:
        block.add_resource(new_resource, resource.term)
        update_parent_resources(block, new_resource)


def create_resources(block):
    for line in block.lines:
        for term in line.terms:
            create_rule = config.create_rule_by_tag.get(term.tag)
            if not create_rule:
                continue

            if skip_term(block, term):
                continue

            for resource in create_rule(term, line, block):
                if not resource:
                    continue

                block.add_resource(resource, term)
                update_parent_resources(block, resource)
