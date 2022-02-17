from moonleap.resource import Resource, ResourceMetaData
from moonleap.utils.fp import uniq


def _create_generic_resource():
    return Resource()


def _get_base_tags(term, block):
    result = []

    for scope in block.get_scopes():
        result.extend(scope.get_base_tags(term))

    return uniq(result)


def create_resource_and_add_to_block(term, block):
    creator_block = block
    if not block.describes(term):
        for competing_block in block.competing_blocks:
            if competing_block.describes(term):
                creator_block = competing_block
                break

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

            resource.meta = ResourceMetaData(
                term, creator_block, _get_base_tags(term, creator_block)
            )

    resource = resource or _create_generic_resource()
    creator_block.add_resource_for_term(resource, term, True)
    if block is not creator_block:
        block.add_resource_for_term(resource, term, False)

    # If a resource appears in the heading of the creator block, then we add
    # it to its parent block as well. In other words, a parent block knows
    # about any resource that is described in its child blocks.
    # This is relevant for certain lookups. For example, if a block mentions
    # foo:bar then this term could be described by some_other_child(up(up(block)).
    # Note that this also creates a symmetry between finding resources and creating
    # them: the blocks that are "competing" for creating the resource are the same
    # blocks where the resource can be found if it already existed.
    if creator_block.describes(term) and creator_block.parent_block:
        creator_block.parent_block.add_resource_for_term(resource, term, False)

    return resource, creator_block
