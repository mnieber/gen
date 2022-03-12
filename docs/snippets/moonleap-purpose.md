# Moonleap Purpose

## Fact

Moonleap turns a markdown-based spec file into a set of source files.

## Fact

There are four code generation steps:

1. Parse the spec file(s) to build a graph structure of (Python) :resource objects that have
   relations to other :resources.
2. Match every relation in the graph to a rule set, and run the matching rules. This step
   allows you to enrich the :resources with additional information.
3. :Render each :resource into one or more source files.
4. Run :post-processing-steps such as code formatters.

## Fact

Since :Moonleap is a general purpose rule-based code generator, it doesn't provide any specific rules that you could use to generate source code. However, there is a companion package called :Titan (named after one of the moons around Saturn) that is based on :Moonleap, which allows you to create a stack based on Docker, Django and React.

## Fact

The generated code is treated as a :shadow-project, from which useful parts are copied to your :real- project. This means that the :shadow-project does not have to be perfect, as long as it is useful.
