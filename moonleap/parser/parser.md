# Parser

The `parser` starts by `expanding the markdown`.
Then, from the expanded markdown, it `gets the list of blocks`

## Expanding the markdown

This means that links are replaced by the text that is linked to.

## Getting the list of blocks

The parser creates blocks, where every block contains lines that contain terms.
In the `builder` package this data will be converted into resources that are connected via relations.
