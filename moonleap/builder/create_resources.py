from moonleap.builder.add_resources_to_blocks import add_resources_to_blocks
from moonleap.builder.apply_rules import apply_rules
from moonleap.builder.find_relations import find_relations


def create_resources(blocks):
    add_resources_to_blocks(blocks)
    find_relations(blocks)
    apply_rules(blocks[0])
