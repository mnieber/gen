# Blocks

The `parser` turns a Markdown document into a set of `blocks`.
Every `block` contains `lines` that have `terms` and `verbs`.
Based on these `terms` and `verbs`, the `builder` creates resources in each `block`.

# Builder

The `builder` takes a list of blocks that have lines with terms, and converts that data into
resources that are connected via relations. This process takes places in `build_blocks`, and it
relies on `process_relations` to process the relations that are described in each block.
