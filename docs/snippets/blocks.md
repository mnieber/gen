# Blocks

## Snippet (./specs/foo/spec.rst)

```
# The foo:project

The foo:project uses the bar:service and the baz:service. :It /shows the welcome:screen.

## The bar:service

The bar:service /has a welcome:endpoint that is /used in the welcome:screen.

### Details

The welcome:screen also /shows a baz:banner.

## The baz:service and its baz:banner

The baz:service /has a welcome:endpoint. :It /defines the baz:banner.
```

## Fact

Every section of the :spec-file defines a block. The section title defines the block title. Here, we see a block with title `The foo:project` and three more blocks with different titles.

## Fact

There are special rules that determine which :blocks describe which :terms. Moonleap uses this information to determine if a :term introduces a new :resource, and to determine which :creation-rules must be used to create it.

## Fact

In general, the question we must answer is: if a :blocks mentions a :term, then which :block is describing that :term? To answer this question we use the notion of "competing blocks". For any block, it's competing blocks are:

- the block itself
- all its (grand)child blocks
- all its (grand)parent blocks
- all direct children of its (grand)parent blocks

The answer to our question is:

1. if a competing block mentions the term it its title, then this block describes the term. If more than one such block can be found then it's considered an error. If no such block is found, then rule 2 (below) is used

2. the competing (grand)parent block that mentions the term and is highest in the tree describes the term.

## Fact

In our example:

1. the first block describes `foo:project` and `welcome:screen`, but (based on rule 1) not `bar:service` or `baz:service`.

2. the second block describes `bar:service` and `welcome:endpoint`. It references the `welcome:screen` from its parent block.

3. The third block references `welcome:screen` and `baz:banner` (because the fourth block is a competing block that mentions `baz:banner` in its title).

4. The fourth block describes `baz:banner`. It also describes a `welcome:endpoint` but this resource is unrelated to the resource in block 2 (this is okay because blocks 2 and 4 are not competing to describe `welcome:endpoint`).

## Fact

The sloppy (but convenient) way to use these rules is to say that:

- among competing blocks (that mention the same term), the block that mentions the term in its title describes it
- among parent and child blocks (that mention the same term), the parent block describes it and the child block references it
- the concept of parent/child is bent a little so that also "the direct child of my (grand)parent can be
  considered my (grand)parent" but we only use this bent concept if that "grand-parent" mentions the term in its title. The mental picture here is that a child block's title explains some detail about its parent block.

## Snippet (./specs/foo/spec.rst)

```
## The baz:service

The baz:service /has a welcome:endpoint. :It /defines the baz:banner^.
```

## Fact

It a term ends with a hat symbol (`baz:banner^`) then it's treated as if that term appeared in the block title. Here, we see how the the block title `The baz:service and its baz:banner` could be replaced by `The baz:service` without affecting the resource creation process.
