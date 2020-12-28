from importlib import import_module

from moonleap.config import config


def create_resources(block):
    for line in block.lines:
        for term in line.terms:
            create_rule = config.create_rule_by_tag.get(term.tag)
            if not create_rule:
                continue

            if term in block.resource_by_term:
                continue

            resource = create_rule(term, line, block)
            block.add_resource(resource, term)


def run_update_rule(block, resource_term, co_resource_term, pgk_path):
    try:
        m = import_module(pgk_path)
    except ImportError as e:
        raise Exception(f"Could not import update rule module: {pkg_path}")

    m.update(block, resource_term, co_resource_term)


def update_resources(block):
    resource_by_term = list(block.resource_by_term.items())
    for resource_term, resource in resource_by_term:
        update_rules = config.get_update_rules(resource)
        for resource_type_id, pkg_sub_path in update_rules:
            pkg_path = ".".join([resource.__module__, pkg_sub_path])
            if resource_type_id is None:
                run_update_rule(block, resource_term, None, pkg_path)
                continue

            for co_resource_term, co_resource in resource_by_term:
                if resource_type_id == co_resource.type_id:
                    run_update_rule(block, resource_term, co_resource_term, pkg_path)
