from moonleap.parser.block import get_extended_scope_names
from moonleap.resource import Resource, ResourceMetaData
from moonleap.resource.forward import create_forward
from moonleap.session import get_session
from moonleap.verbs import is_created_as


def _create_generic_resource(term, block):
    return Resource()


def create_resource_and_add_to_block(term, block):
    creator_block = block
    if not block.describes(term):
        for competing_block in block.competing_blocks:
            if competing_block.describes(term):
                creator_block = competing_block
                break

    resource, forward = None, None

    for scope in block.scopes:
        create_rule, base_tags = scope.find_create_rule(term)
        if create_rule:
            if resource:
                raise Exception(f"More than 1 create rule for {term}")
            resource = create_rule(term, block)
            if resource is None:
                raise Exception(
                    "Resource creation rule returned None: " + str(create_rule)
                )

            resource._meta = ResourceMetaData(term, creator_block, base_tags)
            forward = create_forward(term, is_created_as, term)

    if resource is None:
        resource = _create_generic_resource(term, block)

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

    return resource, forward


def add_meta_data_to_blocks(blocks):
    scope_manager = get_session().scope_manager
    for block in blocks:
        block.scopes = [
            scope_manager.get_scope(scope_name)
            for scope_name in get_extended_scope_names(block)
        ]

    for block in blocks:
        child_blocks = block.get_blocks(include_children=True, include_self=False)
        parent_blocks = block.get_blocks(include_parents=True, include_self=False)
        block.competing_blocks = list(child_blocks)
        for parent_block in parent_blocks:
            sibling_blocks = [x for x in parent_block.child_blocks if x is not block]
            block.competing_blocks += list(sibling_blocks)
