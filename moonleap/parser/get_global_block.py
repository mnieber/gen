from moonleap.parser.block import Block

_global_block = None


def get_global_block():
    global _global_block
    if _global_block is None:
        _global_block = Block(name="global", level=0, scope_names=[])
    return _global_block
