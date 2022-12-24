from moonleap.blocks.term import word_to_term
from moonleap.resource import ResourceMetaData


def get_meta(word, block=None):
    return ResourceMetaData(
        term=word_to_term(word),
        block=block,
        base_tags=[],
    )
