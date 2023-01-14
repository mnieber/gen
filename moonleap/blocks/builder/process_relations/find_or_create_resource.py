from moonleap.blocks.term import Term
from moonleap.resources.named_resource import NamedResource
from moonleap.resources.relations.rel import Rel
from moonleap.utils.case import kebab_to_camel

from .create_resource_in_block import create_resource_in_block, find_describing_block


def find_or_create_resource(block, origin, term):
    from moonleap.blocks.builder.process_relations import process_relations

    has_name = term.name is not None

    # Step 1: find existing resource
    res = _find_resource(term, block)
    if res:
        return res

    # Step 2: if the resource doesn't exist, find the publishing block. Note that the
    # publishing block may be some child of the current block, some parent of the current block
    # or some sibling of some parent block.
    publishing_block = find_describing_block(term, block) or block

    # Step 3: create the resource in the publishing block, and add to current block
    res = create_resource_in_block(term, publishing_block)
    if block is not publishing_block:
        block.add_resource_for_term(res, term, False)

    # Step 4: if a resource appears in the heading of the publishing block, then we add
    # it to its parent block as well. In other words, a parent block knows
    # about any resource that is described in its child blocks.
    # Note that this creates a symmetry between finding resources and creating
    # them: the blocks that are "competing" for creating the resource are the same
    # blocks where the resource can be found if it already existed.
    if publishing_block.describes(term) and publishing_block.parent_block:
        publishing_block.parent_block.add_resource_for_term(res, term, False)

    # Step 5: handle named term
    if has_name:
        if not isinstance(res, NamedResource):
            raise Exception(f"Resource ({res}) is not named")

        res.name = kebab_to_camel(term.name)
        res.typ = find_or_create_resource(
            block,
            origin,
            Term(data=term.data, tag=term.tag, is_title=term.is_title),
        )

    # Step 6: process the _is_created_as relation
    process_relations(
        [
            Rel(
                subj=term,
                verb=_is_created_as,
                obj=term,
                block=publishing_block,
                origin=origin,
            )
        ],
        actions,
    )

    return res


def _find_resource(term, block):
    for parent_block in block.get_blocks(include_self=True, include_parents=True):
        resource = parent_block.get_resource(term)
        if resource:
            return resource
    return None
