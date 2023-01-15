# Scopes

## Snippet (./specs/foo/spec.md)

```
# The foo:project {foo, foobar}

The foo:project uses the bar:service and the baz:service.

## The [bar:service](./bar-service.md)

This body will be replaced (it could have been left empty, as in the block below).

## The [baz:x](./baz-service.md)
```

## Fact

A :block in a :spec-file can specify one or more scopes. These are string values that determine which creation and relation rules are used in the block. Here, the first block has :scopes `foo` and `foobar`.

## Fact

The :settings file specifies a list of :Moonleap-packages for every scope. The creation-rules and relation-rules of those :Moonleap-packages are used to create resources and relations (in all blocks that have that scope).

## Fact

If a block title contains a link then the body of that block is replaced with the contents of that link. This process is called: :expanding the :spec-file. In addition, the name of the linked file is added as a scope to the block. Here, the second block will have scope `bar-service` and the third block will have scope `baz-service`.

## Fact

For debugging purposes, the fully expanded :spec-file is written to the :moonleap-directory.

## Fact

Every block automatically has the `default` scope.

## Snippet (specs/foo/settings.yml)

```
packages_by_scope:
    default:
        - titan.default_pkg
        - titan.project_pkg
    bar-service:
        - bar_pkg
    baz-service: []
    foo: []
    foobar: []
```

## Fact

Here, the :settings file specifies that the `titan.default_pkg` and `titan.project_pkg` are used for all blocks with the `default` scope, and `bar_pgk` is used for blocks with the `bar-service` scope.

## Fact

If a scope has no packages, then it must still be listed in `packages_by_scope` in the :settings file.
