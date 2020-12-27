from config import config


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


def update_resources(block):
    for term, resource in block.resource_by_term.items():
        for update_rule in block.update_ruleset_by_term.get(term.tag) or []:
            update_rule(resource, term, block)
