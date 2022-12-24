# Entrypoint

The Moonleap entrypoint `parses the args` and `checks the args`.
It then creates a `session`.
It either executes a `gen` or a `diff` operation.

## The `gen` operation

The `gen` operation generates code.
It uses the `parser` package to parse the markdown.
It uses the `builder` package to build a graph with all the resources.
It uses the `render` package to convert this graph into source files.
It uses the `report` package to report on the result.
