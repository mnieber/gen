from moonleap.blocks.term import word_to_term
from moonleap.resources.resource import ResourceMetaData


def get_meta(word):
    return ResourceMetaData(
        term=word_to_term(word),
        base_tags=[],
    )
