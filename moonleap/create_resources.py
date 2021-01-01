from importlib import import_module

import ramda as R

from moonleap.config import config
from moonleap.resource import Always


def update_with_child(resource, child_resource):
    update_rules = config.get_update_rules(resource.type_id)
    new_resources = []
    for child_resource_type_id, (update, delay) in update_rules.items():
        if child_resource_type_id == child_resource.type_id:
            for new_resource in update(resource, child_resource) or []:
                new_resources.append(new_resource)
    return new_resources


def add_resource(block, resource, term):
    block.add_resource(resource, term)

    for new_resource in update_with_child(resource, Always()):
        add_resource(block, new_resource, term)

    for child_resource in list(block.get_resources(include_children=True)):
        for new_resource in update_with_child(resource, child_resource):
            add_resource(block, new_resource, term)


def create_resources(blocks):
    for block in R.sort_by(lambda x: -1 * x.level)(blocks):
        for term in reversed(block.get_terms()):
            create_rule = config.create_rule_by_tag.get(term.tag)
            if not create_rule:
                continue

            if term in block.get_terms(include_parents=True, include_self=False):
                continue

            for resource in create_rule(term, block):
                if resource:
                    add_resource(block, resource, term)
