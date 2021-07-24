import ramda as R
from moonleap.builder.add_resources_to_blocks import add_resources_to_blocks
from moonleap.builder.apply_rules import apply_rules
from moonleap.builder.find_relations import find_relations
from moonleap.session import get_session


def _register_contexts(blocks):
    session = get_session()

    for block in R.sort_by(lambda x: x.level)(blocks):
        for context_name in block.context_names:
            session.register_context(context_name)


def create_resources(blocks):
    unmatched_rels = []
    _register_contexts(blocks)
    add_resources_to_blocks(blocks)
    find_relations(blocks)
    apply_rules(blocks[0], unmatched_rels)
    return unmatched_rels
