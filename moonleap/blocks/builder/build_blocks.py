from .add_meta_data_to_blocks import add_meta_data_to_blocks
from .extract_relations import extract_relations
from .process_relations import process_relations
from .run_actions import run_actions


def build_blocks(blocks):
    add_meta_data_to_blocks(blocks)

    actions = []
    for block in blocks:
        process_relations(extract_relations(block), actions)

    run_actions(actions)
