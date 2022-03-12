# The :spec-file

## Snippet (./specs/foo/spec.md)

```
# The bar:module

The bar:module /has a main+todo:list-view and a :router.
```

## Fact

The :spec-file is written in markdown. It's called `spec.md` and is located in the so-called :spec-dir.
Here, the :spec-dir is `./specs`.

## Fact

The purpose of the :spec-file is to describe your project in a way that allows Moonleap to generate source code for it.

## Fact

The most important ingredients of the :spec-file are so-called :terms and :verbs.

## Fact

:Terms are words in the spec that follow a pattern of name+data:tag, where the :term-name and :term-data are optional. Here we see three terms: `bar:module`, `main+todo:list-view` and `:router`.

## Fact

Generally speaking, the :term-tag indicates a resource type (`list-view`), the :term-data indicates a flavour of that type (it's a `list-view` of `todo` elements) and the :term-name indicates a named instance of this resource type (it's an instance of a `todo:list-view` that is named `main`).

## Fact

:Verbs are words that are prefixed with a slash. :Verbs indicate relations between terms. Here there is one verb: `/has`.

## Fact

Moonleap will turn every term (such as `bar:module`) into a Python :resource object. How a term is converted into a resource depends on the :block in which the term appears. See: ref:blocks.

## Fact

Relations between resources (as specified by :verbs) are used to enrich the information in these resources. Here, when we :render the `bar:module` we can use the fact that it has a `main+todo:list-view` and a `:router`.

## Snippet (./specs/foo/spec.md)

```
# The foo:project

The foo:project /has a bar:module and a baz:module. The foo:project /exposes the bar:module.
```

## Fact

Every :relation between :resources is qualified by the :verb that creates the relation. Here, the `foo:project` resource is related twice to the `bar:module` resource: once via `/has` and once via `/exposes`.

## Snippet (./specs/foo/spec.md)

```
## Endpoints

The backend:service and frontend:service /have a welcome:endpoint, status:endpoint and about:endpoint that can be /called from the frontent:service.
```

## Fact

We can specify multiple relations between the resources in a single sentence. All the :resources that appear before the connecting :verb are related to all the :resources that appear after it. Here, the `backend:service` :resource is related (via `/have`) to `welcome:endpoint`, `status:endpoint` and `about:endpoint`. The `frontend:service` is also related to these three resources. Finally, each of `welcome:endpoint`, `status:endpoint` and `about:endpoint` is related to `frontend:service` via `/called`.

## Snippet (./specs/foo/spec.md)

```
## Endpoints

The (backend:service which /connects to :postgres) /has a welcome:endpoint.
```

## Fact

You can use parentheses to limit the visibility of a term. Here, due to the parentheses, there is no relation between `:postgres` and `welcome:endpoint`.

## Fact

The first resources that appears between parentheses acts as the resulting :resource for the parenthesized text. Here, we specified a `/has` relation between `backend:service` (the resulting :resource) and `welcome:endpoint`.

## Snippet (./specs/foo/spec.md)

```
# The bar:module

The bar:module /has a main+todo:list-view. :It also /has a :router.
```

## Fact

The `:it` term refers to the first term in the previous sentence. It offers a useful way to prevent repeating terms. Here, the `:it` term refers back to `bar:module`.

## Snippet (./specs/foo/spec.md)

```
## Endpoints

The goal of the welcome:endpoint is:: to welcome the user.
```

## Fact

To use a colon in the :spec-file without identifying a resource, it needs to be doubled. This is why here, we wrote `is::` instead of `is:`.
