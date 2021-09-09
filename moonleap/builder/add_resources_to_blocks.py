import ramda as R
from moonleap.parser.term import is_generic_term
from moonleap.resource import Resource
from moonleap.session import get_session


def _create_generic_resource(term, block):
    return Resource()


def _create_resource(term, creator_block, scope_manager):
    create_rule = None

    for scope_name in creator_block.scope_names:
        scope = scope_manager.get_scope(scope_name)
        local_create_rule = scope.get_create_rule(term)
        if local_create_rule:
            if create_rule:
                raise Exception(f"More than 1 create rule for {term}")
            create_rule = local_create_rule

    resource = (create_rule or _create_generic_resource)(term, creator_block)
    if resource is None:
        raise Exception(f"Resource creation rule returned None: {create_rule}")
    return resource


def add_resources_to_blocks(blocks):
    session = get_session()

    for block in R.sort_by(lambda x: x.level)(blocks):
        parent_blocks = block.get_blocks(include_parents=True, include_self=False)
        child_blocks = block.get_blocks(include_children=True, include_self=False)
        sibling_blocks = (
            [x for x in block.parent_block.child_blocks if x is not block]
            if block.parent_block
            else []
        )
        competing_blocks = list(child_blocks) + list(sibling_blocks)

        for term in block.get_terms():
            if is_generic_term(term):
                continue

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
                for competing_block in competing_blocks:
                    if competing_block.describes(term):
                        creator_block = competing_block
                        break

            resource = _create_resource(term, creator_block, session.scope_manager)
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
