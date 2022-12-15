from moonleap.parser.block import Block
from moonleap.parser.term import word_to_term
from moonleap.resource import ResourceMetaData

_global_block = None


def get_global_block():
    global _global_block
    if _global_block is None:
        _global_block = Block(name="global", level=0, scope_names=[])
    return _global_block


def get_meta(word, block=None):
    return ResourceMetaData(
        term=word_to_term(word),
        block=block or get_global_block(),
        base_tags=[],
    )
