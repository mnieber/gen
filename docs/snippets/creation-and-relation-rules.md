# :Creation-rules and :relation-rules

## Snippet (`bar_pkg/item/__init__.py`)

```
from moonleap import kebab_to_camel, create, Resource
from dataclasses import dataclass

@dataclass
class Item(Resource):
    item_name: str

@create("item")
def create_item(term):
    return Item(
        item_name=kebab_to_camel(term.data)  # [4]
    )

@create("project:item")
def create_project_item(term):
    return Item(
        item_name="project",
    )
```

## Fact

A (Python) :Moonleap-module contains :creation-rules that convert :terms into Python :resource objects. A :creation-rule is a python function that is decorated with `@create` and returns a :resource.

## Fact

The `@create` decorator contains a term-pattern that can be matched against a term. This pattern can include a name, data and tag pert. Here, the term-pattern is `"item"`.

## Fact

The most specific :creation-rule that matches the :term is used to create the resource for that :term. For the term `project:item`, the match with `create_project_item` is more specific than the match with `create_item`.

## Snippet (`bar_pkg/item/__init__.py`)

```
@rule("graphql:api", "posts", "item")
def graphql_api_posts_item(graphql_api, item):
    item.used_by_api = True
    return [
        create_forward(graphql_api, has, f"post-{item.item_name}:mutation"),
        create_forward(graphql_api, documents, item),
    ]
```

## Fact

A :Moonleap-module can also contains :relation-rules. A :relation-rule has an subject term-pattern, a verb and an object term-pattern. It receives the matching resources as arguments.

## Fact

For every relation between resources that the :spec-file describes, all matching :relation-rules are executed in order to enrich the resources in that relation. Here, we enrich the `item` resource by setting `item.used_by_api = True`.

## Fact

A :relation-rule may return a list of additional relations, which are processed in the same way as the relations in the :spec-file. Here, we return two additional relations.

## Fact

When you return an additional relation, you can use a term to refer to some other resource (`f"post-{item.item_name}:mutation"`) or you can directly insert the resource itself (`item`).

## Snippet (`bar_pkg/item/__init__.py`)

```
@rule("graphql:api", ("posts", "saves"), "item")
def graphql_api_posts_item(graphql_api, item):
    item.used_by_api = True
```

## Fact

Verbs in relation rules can be defined as tuples (here we use `("posts", "saves")`) that contain different variants, so that it makes no difference whether you write /posts or /saves.
