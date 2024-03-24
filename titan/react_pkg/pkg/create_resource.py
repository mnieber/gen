from moonleap.block_builder.find_or_create_resource_in_block import (
    find_or_create_resource_in_block,
)
from moonleap.block_builder.run_actions import run_actions


def create_resource(block, term):
    actions = []
    data_res = find_or_create_resource_in_block(block, term, None, actions)
    run_actions(actions)
    return data_res
