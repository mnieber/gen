from moonleap.session import get_session


def _get_extended_scope_names(root_block):
    scope_names = []
    for block in root_block.get_blocks(include_children=True):
        for scope_name in block.scope_names:
            if scope_name not in scope_names:
                scope_names.append(scope_name)
    return scope_names


def add_meta_data_to_blocks(blocks):
    scope_manager = get_session().ws.scope_manager
    for block in blocks:
        block.set_scopes(_get_scopes(scope_manager, block))

    for block in blocks:
        child_blocks = block.get_blocks(include_children=True, include_self=False)
        parent_blocks = block.get_blocks(include_parents=True, include_self=False)
        block.competing_blocks = list(child_blocks)
        for parent_block in parent_blocks:
            sibling_blocks = [x for x in parent_block.child_blocks if x is not block]
            block.competing_blocks += list(sibling_blocks)


def _get_scopes(scope_manager, block):
    result = []
    for scope_name in _get_extended_scope_names(block):
        scope = scope_manager.get_scope(scope_name)
        if scope:
            result.append(scope)

    return result
