# :Blocks

## Snippet (./specs/foo/spec.rst)

```
# The donations:project (block 1)

The donation:project uses:
- the backend:service and
- the frontend:service.

:It /manages the donation:process.

## The frontend:service (block 2)

The frontend:service /has
- a donations:view that is /used in the donation:process.
- :It has a :readme-doc.

### Details (block 3)

The donations:view
  /run the donations:query.

## The backend:service and the donations:query (block 4)

The backend:service:
- /has a donations:query.
- :It has a :readme-doc.

```

## Fact

Every section of the :spec-file defines a :block. Here, we see a :block with title `The donations:project` and three more :blocks with different titles. Note that this example is a bit contrived to illustrate different (edge) cases.

## Fact

When Moonleap encounters a :term in a :block, then it checks whether a :resource for that :term already exists. If not, then:

- it finds out which :block describes the :term;
- it finds the correct :creation-rule in the :scopes of that block and creates the :resource;
- it finds any addition :rules in the :scopes of that block (that match the :term) and runs them.

## Fact

To find out which :block describes a :term, we use the notion of "competing blocks". For any block, it's competing blocks are:

- the block itself
- all its (grand)child blocks
- all its (grand)parent blocks
- all direct children of its (grand)parent blocks

The answer to our question is:

1. if a competing block mentions the term it its title, then this block describes the term. If more than one such block can be found then it's considered an error. If no such block is found, then rule 2 (below) is used

2. the competing (grand)parent block that mentions the term and is highest in the tree describes the term.

## Fact

In our example:

1. block 1 describes `donation:project` and `donation:process`, but (based on rule 1) not `frontend:service` or `backend:service`.

2. block 2 describes `frontend:service`, `donations:view` and `:readme-doc`. It references the `donation:process` from its parent block.

3. block 3 references `donation:process` and `donations:query` (because block 4 is a competing block that mentions `donations:query` in its title).

4. block 4 describes `donations:query`. It also describes a `:readme-doc` but this resource is unrelated to the `:readme-doc` in block 2. This is okay because blocks 2 and 4 are not competing to describe `:readme-doc`, instead they both refer to their "own" `:readme-doc`.

## Snippet (./specs/foo/spec.rst)

```
## The backend:service

The backend:service /defines the donations:query^.
```

## Fact

It a term ends with a hat symbol (`donations:query^`) then it's treated as if that term appeared in the block title. This allows us to replace the block title `The backend:service and its donations:query` by `The backend:service` without affecting the resource creation process.
