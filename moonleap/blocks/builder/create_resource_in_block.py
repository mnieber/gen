from moonleap.resources.resource import ResourceMetaData
from moonleap.utils.fp import uniq


def _get_base_tags(term, block):
    result = []

    for scope in block.get_scopes():
        result.extend(scope.get_base_tags(term))

    return uniq(result)


def find_describing_block(term, block):
    describing_block = block if block.describes(term) else None
    for competing_block in block.competing_blocks:
        if competing_block.describes(term):
            if describing_block:
                raise Exception("More than 1 publishing block for " + str(term))
            describing_block = competing_block

    return describing_block


def create_resource_in_block(term, block):
    resource = None

    for scope in block.get_scopes():
        create_rule = scope.find_create_rule(term)
        if create_rule:
            if resource:
                raise Exception(f"More than 1 create rule for {term}")

            resource = create_rule(term)
            if resource is None:
                raise Exception(
                    "Resource creation rule returned None: " + str(create_rule)
                )

    if resource:
        register_resource_in_block(term, block, resource)

    return resource


def register_resource_in_block(term, block, resource):
    resource.meta = ResourceMetaData(term, block, _get_base_tags(term, block))
    block.add_resource_for_term(resource, term, True)
