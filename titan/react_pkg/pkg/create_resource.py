from moonleap.blocks.builder.find_or_create_resource import find_or_create_resource
from moonleap.blocks.builder.run_actions import run_actions


def create_resource(block, term):
    actions = []
    data_res = find_or_create_resource(block, term, None, actions)
    run_actions(actions)
    return data_res
