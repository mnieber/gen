from moonleap.block_builder.extract_relations_from_block import (
    extract_relations_from_block,
)

from .add_meta_data_to_blocks import add_meta_data_to_blocks
from .process_relations import process_relations
from .run_actions import run_actions


def build_blocks(blocks):
    add_meta_data_to_blocks(blocks)

    actions = []
    for block in blocks:
        process_relations(extract_relations_from_block(block), actions)

    run_actions(actions)
