# Builder

The `builder` takes a list of blocks that have lines with terms, and converts that data into
resources that are connected via relations. This process takes places in `build_blocks`, and it
relies on `process_relations` to process the relations that are described in each block.
