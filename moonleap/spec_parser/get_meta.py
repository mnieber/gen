from moonleap.resources.resource import ResourceMetaData
from moonleap.spec.term import str_to_term


def get_meta(word):
    return ResourceMetaData(
        term=str_to_term(word),
        block=None,
        base_tags=[],
    )
