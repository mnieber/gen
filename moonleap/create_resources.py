from importlib import import_module

import ramda as R

from moonleap.config import config


def derive_resources(resource):
    new_resources = []
    derive_rules = config.get_update_rules(resource.type_id)
    for derive_rule in derive_rules:
        new_resources += derive_rule(resource)
    return new_resources


def add_resource(block, resource, term):
    block.add_resource(resource, term)

    for new_resource in derive_resources(resource):
        add_resource(block, new_resource, term)


def group_resources(blocks):
    resources = blocks[0].get_resources(include_children=True)

    for a_resource in resources:
        for b_resource in resources:
            if a_resource is b_resource:
                continue

            add_child = b_resource.is_created_in_block_that_describes(a_resource)
            if not add_child:
                for block in blocks:
                    if block.describes(a_resource) or a_resource.block is block:
                        if a_resource.is_paired_with(block, b_resource):
                            add_child = True
                            break

            if add_child:
                a_resource.add_child(b_resource)


def create_resources(blocks):
    for block in R.sort_by(lambda x: -1 * x.level)(blocks):
        for term in reversed(block.get_terms()):
            create_rule = config.create_rule_by_tag.get(term.tag)
            if not create_rule:
                continue

            if term in block.get_terms(include_parents=True, include_self=False):
                # term will be processed by a parent block
                continue

            for resource in create_rule(term, block):
                if resource:
                    add_resource(block, resource, term)

    group_resources(blocks)
