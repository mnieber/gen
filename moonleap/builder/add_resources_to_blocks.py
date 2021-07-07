import ramda as R
from moonleap.builder.config import config
from moonleap.resource import Resource


def _create_generic_resource(term, block):
    return Resource()


def _create_resource(term, creator_block):
    create_rule = config.get_create_rule(term) or _create_generic_resource
    resource = create_rule(term, creator_block)
    return resource


def add_resources_to_blocks(blocks):
    for block in R.sort_by(lambda x: x.level)(blocks):
        parent_blocks = block.get_blocks(include_parents=True, include_self=False)
        child_blocks = block.get_blocks(include_children=True, include_self=False)

        for term in block.get_terms():
            if block.get_resource(term):
                continue

            resource = None

            for parent_block in parent_blocks:
                resource = parent_block.get_resource(term)
                if resource:
                    block.add_resource_for_term(resource, term, False)
                    break

            if resource:
                continue

            creator_block = block
            if not block.describes(term):
                for child_block in child_blocks:
                    if child_block.describes(term):
                        creator_block = child_block
                        break

            resource = _create_resource(term, creator_block)
            creator_block.add_resource_for_term(resource, term, True)
            if block is not creator_block:
                block.add_resource_for_term(resource, term, False)

            # If a resource appears in the heading of the creator block, then we add
            # it to it's parent block as well. In other words, a parent block knows
            # about any resource that is described in its child blocks.
            if (
                creator_block.describes(term)
                and creator_block.parent_block
                and not creator_block.parent_block.get_resource(term)
            ):
                creator_block.parent_block.add_resource_for_term(resource, term, False)
